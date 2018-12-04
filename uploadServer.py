from os.path import join
from flask import Flask, flash, request
from werkzeug.utils import secure_filename
import dash
import dash_html_components as html
import os
cwd = os.getcwd()
UPLOAD_FOLDER = cwd + '\\datasets'
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.layout = html.Div(
        children=[
            html.Iframe(id='iframe-upload',src=f'/upload'),
            html.Div(id='output')
                ]
)


@app.server.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return '''
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
   app.run_server(debug=True, port=8051)