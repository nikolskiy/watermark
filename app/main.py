import os
from flask import Flask, flash, request, redirect, render_template, send_file
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

UPLOAD_FOLDER = '/tmp/watermark'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
root = os.path.dirname(__file__)


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def add_text(im, text, font_name, font_size):
    font_path = os.path.join(root, 'fonts', font_name)

    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(im)
    x = im.size[0] - len(text) * font_size / 2
    y = im.size[1] - (font_size + 20)
    draw.text((x, y), text, font=font)
    return im


def sr(im):
    return add_text(im, 'Test Text', 'AmaticaSC-Bold.ttf', 30)


def parse_input():
    config = dict()
    config['text'] = request.form.get('text')
    config['font_name'] = request.form.get('font_name')
    config['font_size'] = request.form.get('font_size')
    config['as_attachment'] = request.form.get('as_attachment', False)
    return config


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print(parse_input())
            filename = secure_filename(file.filename)
            base, _ = os.path.splitext(filename)
            filename = base + '.jpg'
            im = Image.open(file)
            im.thumbnail((800, 1200), Image.LANCZOS)
            im = sr(im)
            image_io = BytesIO()
            im.save(image_io, 'JPEG', quality=85)
            image_io.seek(0)
            return send_file(
                image_io,
                attachment_filename=filename,
                mimetype='image/jpeg',
                as_attachment=False,
            )

    return render_template('upload.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
