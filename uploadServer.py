from os.path import join
from flask import Flask, flash, request
from werkzeug.utils import secure_filename
import dash
import dash_html_components as html
import time as t
import os
import inspect
from scripts import makeFile

cwd = os.getcwd()
UPLOAD_FOLDER = cwd + '\\datasets'
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.layout = html.Div(
    children=[
        html.Iframe(id='iframe-upload', src=f'/upload'),
        html.Div(id='output')
    ]
)


@app.server.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        try:
            now = t.time()
            file = request.files['file']
            filename = secure_filename(file.filename)
            if ".csv.gz" in filename or ".dat_.gz" in filename or '.txt' in filename:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                if ".csv.gz" in filename:
                    makeFile.csv_gz_to_txt(filename)
                    os.remove(UPLOAD_FOLDER + "/" + filename)
                elif ".dat_.gz" in filename:
                    makeFile.dat_gz_to_txt(filename)
                    os.remove(UPLOAD_FOLDER + "/" + filename)
            print(t.time(), "@", inspect.currentframe().f_code.co_name, "<<<UPLOADING TOOK", t.time() - now,
                  "SECONDS>>>")
        except KeyError:
            pass
    return '''
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
