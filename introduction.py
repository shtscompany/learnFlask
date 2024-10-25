from flask import Flask, render_template

app = Flask(__name__)

# In Jinja2, you can pass Python variables to your templates and render them directly in HTML.
@app.route('/greet/<name>')
def greet(name):
    items = ["Apples", "Bananas", "Cherries"]
    return render_template('index.html', name=name, items=items)


if __name__ == '__main__':
    app.run(debug=True)
