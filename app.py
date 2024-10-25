from flask import Flask, render_template, flash, redirect, url_for
from forms import ContactForm

app = Flask(__name__)




if __name__ == '__main__':
    app.run(debug=True)
