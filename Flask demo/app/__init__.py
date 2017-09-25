#initialises a python module, otherwise the app dir won't be recognised as module

import os
from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename

#init app
app = Flask(__name__, instance_relative_config=True)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

#Load the views
from app import views

#Load the config file
app.config.from_object('config')

#for uploading files
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('upload.html')

@app.route('/uploads/<filename>', methods=['GET', 'POST'])
def get_upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)