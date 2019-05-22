import os
from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

from wtforms import Form, BooleanField, StringField, SelectField, IntegerField, FileField, validators

root = os.path.dirname(__file__)

app = Flask(__name__)


def image_file_is_required(_, field):
    image = request.files.get(field.name)
    if not image.filename:
        raise validators.StopValidation('An image file is required')


def allowed_file_formats(form, field):
    image = request.files[field.name]
    base, ext = os.path.splitext(secure_filename(image.filename))
    if ext.lstrip('.').lower() not in {'png', 'jpg', 'jpeg', 'gif'}:
        raise validators.ValidationError('Invalid image format')
    form.base_image_name = base


class UploadForm(Form):
    text = StringField('Watermark text', [validators.Length(min=2, max=700)], default='Test Text')
    font_name = SelectField('Font name')
    font_size = IntegerField('Font size', [validators.NumberRange(min=5)], default=30)
    as_attachment = BooleanField('Open download dialog', default=False)
    image = FileField(
        'Image',
        [image_file_is_required,
         allowed_file_formats]
    )


def add_text(im, text, font_name, font_size):
    font_path = os.path.join(root, 'fonts', font_name)

    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(im)
    x = im.size[0] - len(text) * font_size / 2
    y = im.size[1] - (font_size + 20)
    draw.text((x, y), text, font=font)
    return im


def convert_image(form):
    im = Image.open(request.files[form.image.name])
    im.thumbnail((800, 1200), Image.LANCZOS)
    im = add_text(im, form.text.data, form.font_name.data, form.font_size.data)
    image_io = BytesIO()
    im.save(image_io, 'JPEG', quality=85)
    image_io.seek(0)
    return image_io


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm(request.form)
    form.font_name.choices = [('AmaticaSC-Bold.ttf', 'AmaticaSC-Bold')]
    form.font_name.default = 'AmaticaSC-Bold.ttf'

    if request.method == 'POST' and form.validate():

        return send_file(
            convert_image(form),
            attachment_filename=form.base_image_name + '.jpg',
            mimetype='image/jpeg',
            as_attachment=form.as_attachment.data,
        )

    return render_template('upload.html', form=form)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
