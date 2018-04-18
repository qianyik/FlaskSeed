from datetime import date
from logging import WARNING

from flask import Flask, Blueprint, request, jsonify, render_template
from flask.ext.restful import abort
from flask_restful import Resource, Api
from sqlalchemy.orm.exc import NoResultFound

from flask_angular_scaffold.models import Project, Contact
from flask_angular_scaffold.api_base import Api_Base

app = Flask(__name__)
fas_bp = Blueprint('fas', __name__)
api = Api(fas_bp)


@api.resource('/project/')
class API_Projects(Resource, Api_Base):
    get_access = 'standard' #These are checked in api_base for permissions
    put_access = 'standard'

    def __init__(self):
        super(API_Projects, self).__init__(Project, request)
        self.object_name = 'Projects'        

    def get(self):
        # Any custom processing will be done here.
        # If custom processing, then will have to decide if you
        # want to use api_base or process directly here.
        # Same with the post, single get, put, and delete (below).
        #
        # Otherwise: this will use abi_base collection_get
        return self.collection_get()

    def post(self):
        return self.collection_post()

@api.resource('/project/<project_id>')
class API_Project_Single(Resource, Api_Base):
    get_access = 'standard'
    put_access = 'standard'

    def __init__(self):
        super(API_Project_Single, self).__init__(Project, request)
        self.object_name = 'Project'        

    def get(self, project_id):
        return self.single_get(project_id)

    def put(self, project_id):
        return self.single_put(project_id)

    def delete(self, project_id):

        # NOTE: api_base.single_delete will permenantly
        # delete from database. Do not use unless you want
        # the row completely gone.
        return self.single_delete(project_id)
