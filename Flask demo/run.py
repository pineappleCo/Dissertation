__author__ = 's1407459'
import os
from flask import render_template, request
from app import app
import rdf_parser

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
    # only text files may be uploaded
    if file.filename.split('.')[1] == 'txt':
        f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(f)
        # parse uploaded PSI-MI data to RDF
        rdf_parser.parse(f)
        return render_template('index.html')

@app.route('/upload/<path:filename>', methods=["GET"])
def download():
    return send_from_directory(directory="downloads", filename=filename)

if __name__ == '__main__':
    app.run()