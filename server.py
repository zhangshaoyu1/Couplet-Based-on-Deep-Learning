from flask import Flask, jsonify, render_template, redirect
from flask_cors import CORS
from model import Model
from gevent.wsgi import WSGIServer
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from forms import LoginForm

CORS(app)
app.config["SECRET_KEY"] = "12345678"

vocab_file = 'C:/Users/Administrator/Desktop/duilian/couplet/vocabs'
model_dir = 'C:/Users/Administrator/Desktop/duilian/models/output_couplet'

m = Model(
    None, None, None, None, vocab_file,
    num_units=256, layers=4, dropout=0.2,
    batch_size=16, learning_rate=0.0001,
    output_dir=model_dir,
    restore_model=True, init_train=False, init_infer=True)


@app.route('/index/<str>', methods=['GET', 'POST'])
def index(str):
    form = LoginForm()
    if form.validate_on_submit():
        input = form.data['headText']
        print(input)
        output = m.infer(' '.join(input))
        output = ''.join(output.split(' '))
        return redirect('index/' + input + "," + output)
    str = str.split(",")
    form.headText.data = str[0]
    form.input.data = str[0]
    form.output.data = str[1]
    return render_template('index.html', title='Sign In', form=form)

http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()
