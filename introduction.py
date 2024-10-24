from flask import Flask

app = Flask(__name__)

# Routes in Flask are defined using the @app.route decorator. You can create different routes for different URLs:
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'This is the About page.'

if __name__ == '__main__':
    app.run(debug=True)
