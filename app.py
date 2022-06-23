# from flask import Flask, render_template, request
# from werkzeug import secure_filename

# app = Flask(__name__)

# @app.route('/upload')
# def upload_file():
#    # return render_template('upload.html')
#    return "hola"

# @app.route('/uploader', methods = ['GET', 'POST'])
# def uploader_file():
#    if request.method == 'POST':
#       f = request.files['file']
#       f.save(secure_filename(f.filename))
#       return 'file uploaded successfully'

# if __name__ == '__main__':
#    app.run(debug = True)

from consolidación_de_campaña_sms import read_files

import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = "/uploads/"

# Create a directory in a known location to save files to.
uploads_dir = os.path.join(app.instance_path, '../uploads')
os.makedirs(uploads_dir, exist_ok=True)


@app.route('/uploadfile', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # save the single "profile" file
        f = request.files.getlist('file')
        for i in f:
            i.save(os.path.join(uploads_dir, secure_filename(i.filename)))
        read_files(uploads_dir, f)
        # profile = request.files['file']
        # profile.save(os.path.join(uploads_dir, secure_filename(profile.filename)))

        # save each "charts" file
        # for file in request.files.getlist('charts'):
        #     file.save(os.path.join(uploads_dir, secure_filename(file.name)))
        # uploads = os.path.join(uploads_dir)

        try:
            filename = "consolidado.xlsx"
            print(uploads_dir)
            print(filename)
            # return send_from_directory(directory=uploads_dir, filename=filename)
            return send_from_directory(directory=uploads_dir, path=filename, as_attachment=True)

        except:
            filename = "REVISAR CANTIDAD CARACTERES" + "consolidado.xlsx"
            print(uploads_dir)
            print(filename) 
            # return send_from_directory(directory=uploads_dir, filename=filename)
            return send_from_directory(directory=uploads_dir, path=filename, as_attachment=True)

        return redirect(url_for('upload'))
    return render_template('upload.html')


# from flask import Flask, redirect, url_for, request, render_template
# from werkzeug.utils import secure_filename
# from consolidación_de_campaña_sms import read_files

# app = Flask(__name__)


# @app.route('/uploader', methods=['GET', 'POST'])
# def uploader_file():
#     if request.method == 'POST':
#         # receive multiple files
#         f = request.files.getlist('file')
#         s = ""
#         files = []
#         for i in f:
#             s += i.filename + "\n"
#             files.append(i.filename)
#             i.save(secure_filename(i.filename))
#             # File(i.filename).save(secure_filename(i.filename))

#         # return 'file uploaded successfully'
#         return read_files(f)
#         # return str(files)

#         # f = request.files['file']
#         # show the file name when uploaded
#         # print(f.filename)
#         # f.save(secure_filename(f.filename))
#         # return 'file uploaded successfully'
#         # return f.filename


# @app.route('/success/<name>')
# def success(name):
#     return 'welcome %s' % name

@app.route('/')
def upload_file():
    return render_template('upload.html')
    # return "hola"


# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         user = request.form['nm']
#         return redirect(url_for('success', name=user))
#     else:
#         user = request.args.get('nm')
#         return redirect(url_for('success', name=user))


if __name__ == '__main__':
    # app.run(debug=False, host="0.0.0.0")
    app.run()
