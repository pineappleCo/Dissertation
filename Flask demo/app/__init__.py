#initialises a python module, otherwise the app dir won't be recognised as module

import os
from flask import Flask
from werzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['txt']) #will be format for PSI-MI

#init app
app = Flask(__name__, instance_relative_config=True)

#Load the views
from app import views

#Load the config file
app.config.from_object('config')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return '''
    <!doctype html>
    <title>Upload new file</title>
    <h1>Upload new file</h1>
    <form method=post enctype=multipart/form-data>
        <p><input type=file name=file>
            <inputtype=submit value=Upload>
    </form>
    '''

