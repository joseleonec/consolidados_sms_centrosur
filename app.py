from consolidación_de_campaña_sms import read_files

import os
import glob

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
main_html = 'upload.html'

app = Flask(__name__)

uploads_dir = os.path.join(app.instance_path, '../uploads')
os.makedirs(uploads_dir, exist_ok=True)


@app.route('/uploadfile', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files.getlist('file')
        for i in f:
            i.save(os.path.join(uploads_dir, secure_filename(i.filename)))
        read_files(uploads_dir, f)
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
    return render_template(main_html)

@app.route('/')
def upload_file():
    # remove files from uploads_ dir folder
    files = glob.glob(uploads_dir + '/*')
    for f in files:
        os.remove(f)
        print("*"*50)
        print("Removed file: " + f)
        print("*"*50)
        
    return render_template(main_html)

if __name__ == '__main__':
    # app.run(debug=False, host="0.0.0.0")
    app.run()
