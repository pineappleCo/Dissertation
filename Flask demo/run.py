__author__ = 's1407459'
import os
from flask import render_template, request
from werkzeug.utils import secure_filename
from app import app

UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(f)
    return render_template('index.html')

if __name__ == '__main__':
    app.run()