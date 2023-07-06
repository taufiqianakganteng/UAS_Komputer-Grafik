from flask import Flask, render_template, request, redirect, url_for
import os
import cv2
import numpy as np

app = Flask(__name__)

IMAGE_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files['image']
        # cek kalo ada gambar, save gambar ke folder images
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('crop_image', filename=filename))
    return render_template('index.html')

@app.route('/crop/<filename>', methods=['GET', 'POST'])
def crop_image(filename):
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if request.method == 'POST':
        image = cv2.imread(image_path)
        
        # data dari form
        position = request.form['position']
        size = int(request.form['size'])
        
        # posisi potong
        if position == 'top left':
            x = 0
            y = 0
        elif position == 'top center':
            x = (image.shape[1] - size) // 2
            y = 0
        elif position == 'top right':
            x = image.shape[1] - size
            y = 0
        elif position == 'center left':
            x = 0
            y = (image.shape[0] - size) // 2
        elif position == 'center':
            x = (image.shape[1] - size) // 2
            y = (image.shape[0] - size) // 2
        elif position == 'center right':
            x = image.shape[1] - size
            y = (image.shape[0] - size) // 2
        elif position == 'bottom left':
            x = 0
            y = image.shape[0] - size
        elif position == 'bottom center':
            x = (image.shape[1] - size) // 2
            y = image.shape[0] - size
        elif position == 'bottom right':
            x = image.shape[1] - size
            y = image.shape[0] - size
        
        cropped_image = image[y:y+size, x:x+size]
        
        # cek size gambar, kalo error lempar error
        if cropped_image.shape[0] < size or cropped_image.shape[1] < size:
            error_message = "Ukuran gambar hasil potongan kurang dari ukuran yang ditentukan."
            return render_template('index.html', error_message=error_message)
        
        # gambar hasil crop
        cropped_filename = 'cropped_' + filename
        cropped_image_path = os.path.join(app.config['UPLOAD_FOLDER'], cropped_filename)
        cv2.imwrite(cropped_image_path, cropped_image)
        return render_template('index.html', image=filename, cropped_image=cropped_filename)

    return render_template('index.html', image=filename)

if __name__ == '__main__':
    app.run(debug=True)
