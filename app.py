import matplotlib.pyplot as plt
import os
from flask import Flask, flash, request, redirect, url_for
from flask import render_template, send_from_directory
from flask import jsonify

from pydicom import dcmread
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'dcm'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.add_url_rule("/uploads/<name>", endpoint="download_file", build_only=True)

JOBS = [
  {
    "id": 1,
    "title": "Data Analyst",
    "location": "Calgary, AB",
    "salary": "$65,000"
  },
  {
    "id": 2,
    "title": "Data Scientist",
    "location": "Edmonton, AB",
    "salary": "$85,000"
  },
  {
    "id": 3,
    "title": "Web Developer",
    "location": "Edmonton, AB",
  },
  {
    "id": 4,
    "title": "Back End Engineer",
    "location": "Calgary, AB",
    "salary": "$115,000"
  },
]


@app.route("/")
def hello_world():
  return render_template("home.html", jobs=JOBS)


@app.route("/api/jobs")
def list_jobs():
  return jsonify(JOBS)


def allowed_file(filename):
  return '.' in filename and \
         filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
  if request.method == 'POST':
    # check if the post request has the file part
    if 'file' not in request.files:
      flash('No file part')
      return redirect(request.url)
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
      flash('No selected file')
      return redirect(request.url)
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      # ds = dcmread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      # patient_id = ds.PatientID
      return display_file(filename)

  return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/uploads/<name>')
def display_file(name):
  ds = dcmread(os.path.join(app.config['UPLOAD_FOLDER'], name))
  patient_id = ds.PatientID
  # arr = ds.pixel_array
  # plt.imshow(arr, cmap="gray")
  # display = plt.show()
  return render_template("displayscan.html", scan=ds, patient=patient_id)

  # return send_from_directory(app.config["UPLOAD_FOLDER"], name)


if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True)
