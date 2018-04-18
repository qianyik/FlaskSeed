import os

from flask import Flask, request

# Initiate app
app = Flask(__name__)
app._static_folder = os.path.abspath(os.path.dirname(__file__)) +'/static/'
app.debug= True

# Register our routes
from flask_angular_scaffold.api_views import fas_bp
app.register_blueprint(fas_bp,url_prefix='/api')

from flask_angular_scaffold.views import main
app.register_blueprint(main)
