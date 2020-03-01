"""
Question
----------
Using Peexoo.ai as a case study, how do you intend to make it better using your knowledge on A.I

Solution
----------
This is a simple application that implements the barest "Find faces" feature
(Makes use of the luxand.cloud API)

1. Simple Page to upload(register) photo(s) to a name
2. Can search for all users contained in a photo
3. Hosted on Heroku at https://peexoo-find.herokuapp.com


NOTE: There are some constraints to this simple web app:
 - There is no user system, so whenever registering a photo, use the same Name
 else it will be accredited as a new label class

"""
import os
import sys
import requests
import uuid
import json
from flask import Flask, redirect, render_template, request, session, url_for, flash
from flask import send_from_directory
from luxand import luxand

LUXAND_KEY = "f157f049260a4c27a55d4d9935d2952e"
LUXAND_HEADER = { 'token': LUXAND_KEY }
client = luxand(LUXAND_KEY)
main_dir = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(main_dir, "solutions", "templates")
STATIC_DIR = os.path.join(main_dir, "solutions", "static")
assets_dir = os.path.join(main_dir, "assets")
app = Flask(__name__, template_folder=TEMPLATE_DIR, 
            static_url_path="/static",
            static_folder=STATIC_DIR)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config["UPLOAD_FOLDER"] = os.path.join(assets_dir, "uploads")


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    return render_template('index.html')

@app.route('/find', methods=['GET', 'POST'])
def find():
    return render_template('find.html', photos={})

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        if not os.path.exists(app.config["UPLOAD_FOLDER"]):
            os.makedirs(app.config["UPLOAD_FOLDER"])
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name))
    return json.dumps({'filename':f_name})

@app.route('/register', methods=['POST'])
def register():
    name = request.form['Name']
    names, ids = get_persons()
    photos = []
    for _, _, filenames in os.walk(app.config["UPLOAD_FOLDER"]):
        for filename in filenames:
            if not ".gitkeep" in filename:
                print(filename)
                photos.append(os.path.join(app.config["UPLOAD_FOLDER"], filename))
    try:
        if name in names:
            selected_id = ids[names.index(name)]
            for photo in photos:
                client.add_photo_to_person(selected_id, photo)
            flash(f"Registered Image(s) succesfully to {name}", "success")
        else:
            client.add_person(name=name, photos=photos)
            flash(f"Registered Image(s) succesfully to New Person {name}", "success")
    except Exception as e:
        flash(e, "error")
    for i in photos:
        os.remove(i)
    return render_template('index.html')

@app.route('/recognize', methods=['POST'])
def recognize():
    photo = None
    for _, _, filenames in os.walk(app.config["UPLOAD_FOLDER"]):
        photo = os.path.join(app.config["UPLOAD_FOLDER"], filenames[0])
    if photo:
        results = client.recognize(photo=photo)
        os.remove(photo)
        try:
            results[0]
        except KeyError:
            flash(f"Could not recognize photo", "error")
            return render_template('find.html', photos={})
        photos = {}
        for result in results:
            name = result["name"]
            probability = result["probability"]
            iden = result["id"]
            if probability > 0.5:
                flash(f"Recognized as {name} with {round(probability, 2)*100}% certainty", "success")
                photos[name] = get_photos_from_id(iden)
        return render_template('find.html', photos=photos)
    else:
        return render_template('find.html', photos={})

@app.route('/favicon')
def favicon():
    return send_from_directory(assets_dir,
                          'peexoo-logo.ico',mimetype='image/vnd.microsoft.icon')

@app.route('/logo')         
def logo():
    return send_from_directory(assets_dir,
                          'peexoo-logo.png',mimetype='image/png')


def get_persons() -> [list, list]:
    """
    Return all the registered people
    """
    url = "https://api.luxand.cloud/subject"

    payload = {}
    

    response = requests.request("GET", url, data=payload, headers=LUXAND_HEADER)
    persons = []
    ids = []
    for i in response.json():
        persons.append(i["name"])
        ids.append(i["id"])
    return persons, ids

def get_photos_from_id(id):
    """
    Gets all photos from id
    """
    url = f"https://api.luxand.cloud/subject/{str(id)}"

    payload = {}
    headers = { 'token': "f157f049260a4c27a55d4d9935d2952e" }

    response = requests.request("GET", url, data=payload, headers=headers)

    photos = []
    for i in response.json():
        if i.get('url', None):
            photos.append(i.get('url'))
    return photos

if __name__ == '__main__':
    if len(sys.argv) > 1 :
        app.run(debug=True, port=sys.argv[1])
    else:
        app.run(debug=True)
