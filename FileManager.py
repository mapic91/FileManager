from flask import Flask, url_for, request, render_template, redirect, send_from_directory
from werkzeug.utils import secure_filename
import os
import re
import mimetypes
import shutil
import base64
from urllib import parse

root_path = os.getenv("FileManager_Root_Path")
passwod = os.getenv("FileManager_Login_Password")
aria2_path = os.getenv("aria2_path")
password_error_count = 0
max_password_error_count = 5
app = Flask(__name__)
app.config['UPLOAD_FOLODER'] = root_path

def tryint(s):
    try:
        return int(s)
    except:
        return s


def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [tryint(c) for c in re.split('([0-9]+)', s.name)]


def sort_names(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)


def decodestr(strdata):
    return parse.unquote(base64.b64decode(strdata.encode(encoding='ascii')).decode(encoding='ascii'))


class DirEntryInfo:
    def __init__(self, name, size='-', mimetype='-'):
        self.name = name
        self.size = size
        self.mimetype = mimetype is None and 'unknown' or mimetype


def get_dirs_files(path):
    dirs = []
    files = []
    try:
        for entry in os.scandir(path):
            if entry.is_dir():
                dirs.append(DirEntryInfo(entry.name))
            elif entry.is_file():
                files.append(DirEntryInfo(entry.name, entry.stat().st_size,
                                          mimetypes.guess_type(os.path.join(root_path, entry.name))[0]))
    except FileNotFoundError:
        pass
    return dirs, files


def get_path_parts(path):
    parts = [{'part': 'root', 'path': ''}]  # first root path
    combined = ''
    for part in path.split(sep='/'):
        if part != '':
            combined = combined + part + '/'
            parts.append({'part': part, 'path': combined})
    return parts


def delete_all_content_in_folder(path):
    for entry in os.scandir(path):
        if entry.is_dir():
            shutil.rmtree(os.path.join(path, entry.name), ignore_errors=True)
        elif entry.is_file():
            os.remove(os.path.join(path, entry.name))


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = None
    global password_error_count
    if request.method == 'POST':
        if password_error_count < max_password_error_count and request.form.get('pwd', '') == passwod:
            redirect_to_index = redirect(request.args.get('next', '/'))
            response = app.make_response(redirect_to_index)
            response.set_cookie('pwd', value=passwod, max_age=99999999)
            return response
        else:
            password_error_count += 1
            msg = "Password not correct."
    return render_template('login.html', msg=msg)


def not_login():
    return request.cookies.get('pwd') != passwod


def to_login(current_path):
    return redirect(url_for('login', next=current_path))


@app.route('/', methods=['GET'])
def index():
    if not_login():
        return to_login(request.full_path)

    request_path = decodestr(request.args.get('path', ''))
    if request.args.get('delete', '') == '1':
        if request.args.get('dir', '') == '1':
            shutil.rmtree(os.path.join(root_path, request_path), ignore_errors=True)
            return 'OK'
        else:
            os.remove(os.path.join(root_path, request_path))
            return 'OK'
    elif request.args.get('deleteall', '') == '1':
        delete_all_content_in_folder(os.path.join(root_path, request_path))
        return 'OK'
    elif request.args.get('rename', '') == '1':
        oldname = decodestr(request.args.get('oldname', ''))
        newname = decodestr(request.args.get('newname', ''))
        if oldname != '' and newname != '':
            os.rename(os.path.join(root_path, request_path, oldname),
                      os.path.join(root_path, request_path, newname))
            return 'OK'
    else:
        abs_path = os.path.join(root_path, request_path)
        dirs, files = get_dirs_files(abs_path)
        sort_names(dirs)
        sort_names(files)
        space = shutil.disk_usage(root_path)
        usage_str = str.format("{0:.2f}/{1:.2f}GB[{2:.0%}]>>Free:{3:.2f}GB",
                               space.used / 1024 / 1024 / 1024,
                               space.total / 1024 / 1024 / 1024,
                               space.used / space.total,
                               space.free / 1024 / 1024 / 1024, )
        return render_template('index.html', path_parts=get_path_parts(request_path), path=request_path, dirs=dirs,
                               files=files, usage_str=usage_str)


@app.route('/deletselections', methods=['POST'])
def deletselections():
    if not_login():
        return to_login(request.full_path)
    else:
        paths = request.get_json()
        if paths is not None:
            for item in paths:
                if item['type'] == 'floder':
                    shutil.rmtree(os.path.join(root_path, item['value']), ignore_errors=True)
                elif item['type'] == 'file':
                    os.remove(os.path.join(root_path, item['value']))
        return 'OK'


@app.route('/download/<path:filename>', methods=['GET'])
def downloadfile(filename):
    return send_from_directory(root_path, filename=filename)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if not_login():
        return to_login(request.full_path)
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLODER'], filename))
        return redirect(request.url)
    return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
          <p><input type=file name=file>
             <input type=submit value=Upload>
        </form>
        '''


@app.route('/aria2/', defaults={'filename': None}, methods=['GET'])
@app.route('/aria2/<path:filename>', methods=['GET'])
def aria2(filename):
    if not_login():
        return to_login(request.full_path)
    filename = filename or 'index.html'
    return send_from_directory(aria2_path, filename=filename)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, ssl_context=('server.crt','server.key'))
