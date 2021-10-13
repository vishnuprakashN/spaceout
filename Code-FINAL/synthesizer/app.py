from flask import Flask, render_template, request
from model import output
import random
import string


app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        text = request.form['speech']
        voice = request.form['slct']
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(6))
        name = result_str
        output(text,voice,name)
        return render_template('output.html',verify = "yes",file_name = "http://127.0.0.1:5000/static/recordings/{0}.mp3".format(result_str))
    else:
        return render_template('output.html')

if __name__ == "__main__":
    app.run(debug=True)
