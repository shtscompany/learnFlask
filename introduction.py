from flask import Flask
from flask import render_template

# app = Flask(__name__)

# Routes in Flask are defined using the @app.route decorator. You can create different routes for different URLs:
@app.route('/')
def hello_world():
    return 'Hello, World!'

# The @app.route('/') decorator binds the '/' URL (the homepage) to the home() function.
@app.route('/home')
def home():
    return "Hello, Home!"


@app.route('/about')
def about():
    return 'This is the About page.'


# #######################################################################################
# Dynamic Routes: Flask allows you to create dynamic routes, where parts of the URL can act as variables.
# <name> is a dynamic part of the URL. You can visit /user/John to see "Hello, Shota!".
@app.route('/user/<name>')
def user_profile(name):
    return f"Hello, {name}!"

# use templates
@app.route('/user/<name>')
def user_profile_template(name):
    return render_template('index.html', name=name)


if __name__ == '__main__':
    app.run(debug=True)
