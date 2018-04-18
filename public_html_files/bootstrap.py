class CleanScriptName():
    '''
    Fix the SCRIPT_NAME variable

    :param app: the WSGI application
    '''
    def __init__(self, app, script_name = None):
        self.app = app
        self.script_name = script_name

    def __call__(self, environ, start_response):
        if self.script_name is not None:
            environ['SCRIPT_NAME'] = self.script_name
            path_info = environ.get('PATH_INFO', '')
            if path_info.startswith(self.script_name):
                environ['PATH_INFO'] = path_info[len(self.script_name):]
        return self.app(environ, start_response)

if __name__ == '__main__':
    #from flup.server.fcgi import WSGIServer
    from flup.server.cgi import WSGIServer
    import cgitb
    cgitb.enable()
    try:
        from flask_angular_scaffold.app import app
        app.debug = True
        server = WSGIServer(CleanScriptName(app, '/flask_angular_scaffold')).run()
    except Exception as e:
        import logging
        logging.basicConfig()
        logging.getLogger(__name__).exception(e)
