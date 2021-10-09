from flask import Flask, render_template, request
from model import output

app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        text = request.form['speech']
        voice = request.form['voices']
        output(text,voice)
        return render_template('output.html')
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
