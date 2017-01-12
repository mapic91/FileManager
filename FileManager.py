from flask import Flask, url_for, request, render_template
import os
import mimetypes
import shutil

root_path = 'root/web'
app = Flask(__name__)


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


def delete_all_content_in_folder(path):
    for entry in os.scandir(path):
        if entry.is_dir():
            shutil.rmtree(os.path.join(path, entry.name), ignore_errors=True)
        elif entry.is_file():
            os.remove(os.path.join(path, entry.name))


@app.route('/', methods=['GET'])
def index():
    request_path = request.args.get('path', '')
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
        oldname = request.args.get('oldname', '')
        newname = request.args.get('newname', '')
        if oldname != '' and newname != '':
            os.rename(os.path.join(root_path, request_path, oldname),
                      os.path.join(root_path, request_path, newname))
            return 'OK'
    else:
        abs_path = os.path.join(root_path, request_path)
        dirs, files = get_dirs_files(abs_path)
        return render_template('index.html', path=request_path, dirs=dirs, files=files)

if __name__ == "__main__":
    root_path = 'E:/temp/test'
    app.run(debug=True)
