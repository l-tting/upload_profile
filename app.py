from flask import Flask, request, redirect, url_for, render_template_string,session
import os
from model import app,db,Image


# Set the upload folder path dynamically
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static/images')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)



@app.route('/')
def upload_form():
    return '''
    <!doctype html>
    <title>Upload an Image</title>
    <h1>Upload an Image</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        file_url = url_for('static', filename=f'images/{filename}', _external=True)
        new_image = Image(file = file_url)
        db.session.add(new_image)
        db.session.commit()
        return render_template_string('''
        <!doctype html>
        <title>Image Uploaded</title>
        <h1>Image Uploaded Successfully</h1>
        <div>
            <h2>Profile Picture</h2>
            <div style="width: 150px; height: 150px;">
                <img src="{{ file_url }}" style="width: 100%; height: 100%; object-fit: cover;">
            </div>
        </div>
        <a href="/">Upload another image</a>
        ''', file_url=file_url)

if __name__ == '__main__':
    app.run(debug=True)
