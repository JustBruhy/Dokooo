from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('site.html')


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/create/')
def register():
    return render_template('create.html')

@app.route('/login/')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run()
