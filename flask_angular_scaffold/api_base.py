import datetime
from logging import WARNING
import json

from flask import request, jsonify, current_app as app
from flask.ext.restful import abort
from sqlalchemy.exc import OperationalError

from flask_angular_scaffold.database import Session
import flask_angular_scaffold.models as models

class Api_Base(object):
    record_count = 0

    def __init__(self, table_class, request):
        self.table_class = table_class
        self.request = request
        self.Session = Session

    def _check_access(self, access_lvl):
        if 'UFShib_Shib_Session_ID' in request.environ:
            # TODO: check for admin psrole
            return True

        correct_key = app.config.get('STANDARD_API_KEY')
        correct_admin_key = app.config.get('ADMIN_API_KEY')
        provided_key = request.values.get('api_key') or request.headers.get('api_key') \
            or request.get_json().get('api_key')

        if not provided_key or not correct_admin_key or not correct_key:
            app.logger.log(WARNING, "Could not find api key or api key not provided.")
            return False

        if provided_key == correct_admin_key:
            return True
        elif access_lvl == 'admin':
            app.logger.log(
                WARNING,
                "A user attempted to access something for admins with this key: ".format(provided_key)
            )
            return False
        elif provided_key == correct_key:
            return True
        else:
            return False

    def _search(self, table):
        DBSession = self.Session()
        req = self.request.args
        sql = DBSession.query(table)

        embed_keys_list = req.get('embed', '').split(',')
        for key in embed_keys_list:
            if "_embed_{0}".format(key) in dir(self):
                sql = getattr(self, "_embed_{0}".format(key))(sql)

        exclude_keys = [
            'api_key',
            'embed',
            'sort',
            'start_index',
            'page_size',
            'filter']
        search_keys = set([k for k in req.keys() if k not in exclude_keys])

        for key in search_keys:
            search_list = req.getlist(key)

            if hasattr(table, key):
                if len(search_list) > 1:
                    sql = sql.filter(getattr(table, key).in_(search_list))
                elif len(search_list) == 1:
                    sql = sql.filter(getattr(table, key).like(search_list[0]))
                else:
                    continue
            else:
                sql = sql.filter('{0} like "{1}"'.format(key, search_list))

        filters_array = req.getlist('filter')
        for filter in filters_array:
            sql = sql.filter(filter)

        sort_array = self._sort(sort_name="sort")
        for sort in sort_array:
            sql = sql.order_by(sort)

        # TODO: Need to fix this before we can do embedding.
        # sql = sql.group_by(getattr(table, inspect(table).primary_key[0].name))
        try:
            self.record_count = sql.count()
        except OperationalError:
            raise ApiQueryError('Your parameters are not formed properly.')

        if req.get('start_index') and req.get('page_size'):
            sql = sql.limit(req.get('page_size')).offset(req.get('start_index'))

        try:
            return sql.all()
        except OperationalError:
            raise ApiQueryError('Your parameters are not formed properly.')

    def _sort(self, sort_name="sort"):
        query_sort_array = self.request.args.get(sort_name, '').split(',')
        sort = []
        for key in query_sort_array:
            sort_by = key[1:] if key[:1] in ('-', '+', ' ') else key
            sort_array = sort_by.split('.')

            if len(sort_array) == 1:
                if hasattr(self.table_class, sort_by):
                    sort_obj = getattr(self.table_class, sort_by)
                else:
                    continue
            elif len(sort_array) == 2:
                class_obj = getattr(models, sort_array[0].title())
                sort_obj = getattr(class_obj, sort_array[1])
            else:
                continue

            if key[:1] in ('+', ' '):
                sort.append(sort_obj.asc())
            else:
                sort.append(sort_obj.desc())

        return sort

    def collection_get(self):
        #if not self._check_access(self.get_access):
            #abort(403)

        results = self._search(self.table_class)

        if results:
            if hasattr(results[0], '_fields'):
                return_list = [dict(
                    # r[0] - First item in the result tuple which should
                    #   be the original object searched.
                    r[0].to_dict().items() + {
                        l.lower(): getattr(r, l).to_dict() if getattr(r, l) else {}
                        for l in r._fields[1:]
                    }.items()
                ) for r in results]
            else:
                return_list = [r.to_dict() for r in results]
        else:
            return_list = []

        return jsonify({"data": return_list, "total_record_count": self.record_count})

    def collection_post(self):
        DBSession = self.Session()
        #if not self._check_access(self.post_access):
            #abort(403)

        post = self.request.form or self.request.data
        post = json.loads(post)
        attrs = {k: v for k, v in post.iteritems() if k in self.table_class.__table__.columns}
        result = self.table_class(**attrs)
        DBSession.add(result)
        DBSession.commit()
        DBSession.add(result)

        return jsonify({"data": result.to_dict()})

    def single_get(self, table_id):
        DBSession = self.Session()
        #if not self._check_access(self.get_access):
            #abort(403)

        result = DBSession.query(self.table_class).get(table_id)

        if result:
            return jsonify({"data": result.to_dict()})
        abort(404)

    #NOTE: This will permenantly remove row from database.
    def single_delete(self, table_id):
        DBSession = self.Session()
        #if not self._check_access(self.delete_access):
            #abort(403)

        result = DBSession.query(self.table_class).get(table_id)
        DBSession.delete(result)
        DBSession.commit()
        return jsonify({"data": {"message": "The resource has been deleted."}})

    def single_put(self, table_id):
        DBSession = self.Session()
        #if not self._check_access(self.put_access):
            #abort(403)

        result = DBSession.query(self.table_class).get(table_id)

        if not result:
            abort(404)

        post = self.request.form or self.request.get_json()
        for field, value in post.iteritems():
            if hasattr(result, field):
                if field in result.timestamp_representations:
                    value = datetime.datetime.now()
                setattr(result, field, value)

        DBSession.add(result)
        DBSession.commit()
        return jsonify({"data": {"message": "The resource has been updated."}})

class ApiQueryError(Exception):
    pass

