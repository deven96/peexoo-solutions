"""
Question
----------
Using Peexoo.ai as a case study, how do you intend to make it better using your knowledge on A.I

Solution
----------
This is a simple application that implements the barest "Find my face" feature
(Makes use of the luxand.cloud API)

1. Simple Page to upload(register) one's photo(s)
2. Can search for pictures containing using a photo
3. Hosted on Heroku at https://peexoo-find.herokuapp.com
"""
import os
from flask import Flask, redirect, render_template, request, session, url_for
from flask_dropzone import Dropzone
from flask import send_from_directory

main_dir = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(main_dir, "solutions", "templates")
assets_dir = os.path.join(main_dir, "assets")
app = Flask(__name__, template_folder=TEMPLATE_DIR)
dropzone = Dropzone(app)

app.config['SECRET_KEY'] = 'supersecretkeygoeshere'

# Dropzone settings
app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*'
app.config['DROPZONE_REDIRECT_VIEW'] = 'results'

# Uploads settings
app.config['UPLOADED_PHOTOS_DEST'] = assets_dir


@app.route('/', methods=['GET', 'POST'])
def upload_file():
        # set session for image results
    if "file_urls" not in session:
        session['file_urls'] = []
    # list to hold our uploaded image urls
    file_urls = session['file_urls']

    # handle image upload from Dropszone
    if request.method == 'POST':
        file_obj = request.files
        for f in file_obj:
            file = request.files.get(f)
            
        session['file_urls'] = file_urls
        return "uploading..."
    # return dropzone template on GET request 
    return render_template('index.html')

@app.route('/results')
def results():
    
    # redirect to home if no images to display
    if "file_urls" not in session or session['file_urls'] == []:
        return redirect(url_for('index'))
        
    # set the file_urls and remove the session variable
    file_urls = session['file_urls']
    session.pop('file_urls', None)
    
    return render_template('show_uploads.html', file_urls=file_urls)

@app.route('/favicon')
def favicon():
    return send_from_directory(assets_dir,
                          'peexoo-logo.ico',mimetype='image/vnd.microsoft.icon')

@app.route('/logo')         
def logo():
    return send_from_directory(assets_dir,
                          'peexoo-logo.png',mimetype='image/png')
if __name__ == '__main__':
    app.run(debug=True)