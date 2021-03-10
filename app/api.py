import os
import random
import string
from flask import Flask, render_template, jsonify, redirect, request, session, url_for, flash
from werkzeug.utils import secure_filename


WORKING_DIR = os.path.dirname(os.path.abspath(__file__))

ALLOWED_EXTENSIONS = ('png', 'jpg', 'jpeg', 'gif', 'heic')
UPLOAD_FOLDER = os.path.join(WORKING_DIR, 'static/user_images')

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'super_secret_key')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB


def generate_random_str(N=8):
    return ''.join(random.choices(string.ascii_lowercase, k=N))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def parse_bool(_str):
    if type(_str) == bool:
        return _str
    return _str.lower() in ['true', '1', 't', 'y', 'yes']


@app.route('/upload', methods=['POST'])
def upload():
    age = int(request.form['age'])
    star = request.form.get('star')
    star = 'true' if star else 'false'
    name = request.form['name']
    interests = request.form['interests']
    args = {'age': age, 'name': name, 'interests': interests, 'star': star}
    if 'file' not in request.files:
        #flash('No file uploaded')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        #flash('No file uploaded')
        return redirect(request.url)
    elif not allowed_file(file.filename):
        pass
        #flash('Format not supported')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        extension = os.path.splitext(filename)[1]
        filename = generate_random_str() + '.img' + extension
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # return redirect(f'/{filename}', messages=args)
        return redirect(url_for('index', filename=filename, **args))
    return redirect('/')


@app.route('/', methods=['GET'])
@app.route('/<filename>', methods=['GET'])
def index(filename='test_dt.png'):
    flash('You were successfully logged in')

    filename = os.path.join('/static/user_images', filename)
    name = request.args.get('name', 'Donald').title()
    try:
        age = int(request.args.get('age'))
    except:
        age = 74
    try:
        interests = list(filter(bool,
                                [x.strip(' ').title() for x in request.args.get(
                                    'interests').split(';')]
                                ))
    except:
        interests = None
    if not interests:
        interests = ['Politics', 'Party',
                     'Money', 'Golf', 'Flirting on Tinder']

    star = parse_bool(request.args.get('star', 'true'))

    return render_template('tinder.html',
                           name=name,
                           age=age,
                           interests=interests,
                           star=star,
                           filename=filename)


@app.route('/privacy_policy', methods=['GET'])
def privacy_policy():
    return render_template('privacy.html')


@app.route('/blog', methods=['GET'])
def blog():
    return render_template('blog.html')
