from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/user/sing-in')
def login():
    return render_template('login.html')

@app.route('/user/sing-up')
def register():
    return render_template('register.html')

@app.route('/sing-in')
def signing():
    return render_template('login.html')

@app.route('/sing-up')
def signup():
    return render_template('register.html')

@app.route('/business')
def business():
    return render_template('business.html')

@app.route('/explore')
def explore():
    return render_template('explore.html')

@app.route('/docs')
def documentation():
    return render_template('documentation.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

if __name__== '__main__':
    app.run(debug=True)