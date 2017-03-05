from flask import Flask, url_for, request, render_template
import os
import mimetypes
import shutil
import base64
from urllib import parse

root_path = os.getenv("FileManager_Root_Path")
app = Flask(__name__)


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


@app.route('/', methods=['GET'])
def index():
    host = request.host.split(sep=':')[0]
    download_server = 'http://' + host + ':3000'
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
        space = shutil.disk_usage(root_path)
        usage_str = str.format("{0:.2f}/{1:.2f}GB  {2:.2%}",
                               space.used/1024/1024/1024,
                               space.total/1024/1024/1024,
                               space.used/space.total)
        return render_template('index.html', path_parts=get_path_parts(request_path), path=request_path, dirs=dirs,
                               files=files, usage_str = usage_str, download_server=download_server)


if __name__ == "__main__":
    app.run(debug=True)
