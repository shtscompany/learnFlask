# Forms and User Input Handling

Learn how to create and process HTML forms.
Use Flask’s request object to handle form data, including POST requests for submitting sensitive data.
[Flask-WTF (Flask-WTForms) library](https://flask-wtf.readthedocs.io/en/1.2.x/#user-s-guide): Simplifies form handling by providing built-in form validation and CSRF protection.
Example topics: Creating forms, validating input, handling errors, redirecting on form submission.

## How to make it

For this example, we'll use **Flask-WTF** (Flask-WTForms), which provides form handling and validation functionality with CSRF protection (to prevent Cross-Site Request Forgery).

### 1. Setting Up Flask-WTF

First, install Flask-WTF:
```bash
pip install Flask-WTF
```

### 2. Basic Flask Application with a Form

Let's create a simple Flask app with a form using Flask-WTF.

#### File Structure

Here's the file structure for our example:
```
your_project/
│
├── app.py            # Main Flask application
├── forms.py          # Form classes
└── templates/
    └── index.html    # HTML form template
```

### Step 1: Create a Form Class in `forms.py`

In `forms.py`, create a form using `FlaskForm` from Flask-WTF, which will define the fields and validation rules.

```python
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')
```

- **`name`** and **`email`** fields are both required.
- The **`email`** field also has an `Email()` validator, which ensures the input is a valid email address.
- **`submit`** is a button to submit the form.

### Step 2: Set Up the Flask Application in `app.py`

In `app.py`, configure Flask to handle form submissions and CSRF protection.

```python
from flask import Flask, render_template, flash, redirect, url_for
from forms import ContactForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Required for CSRF protection

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ContactForm()
    if form.validate_on_submit():
        # Get the form data
        name = form.name.data
        email = form.email.data

        # Process form data (e.g., save to database, send email, etc.)
        # Here, we're just flashing a success message for simplicity.
        flash(f'Success! Name: {name}, Email: {email}', 'success')
        
        # Redirect to home page or another page
        return redirect(url_for('index'))

    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
```

- **`SECRET_KEY`**: Required for CSRF protection; you should use a secure, unique key for your app.
- **`validate_on_submit()`**: Checks if the form is submitted and all validators pass.
- **`flash()`**: Shows a message on the page. This can be displayed in the template.
- **`redirect()`**: Redirects the user to the given route after a successful submission to prevent form resubmission.

### Step 3: Create the Template `index.html` in the `templates` Folder

In `index.html`, create an HTML form that uses Flask-WTF’s helper functions to render the form fields and display validation messages.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Contact Form</title>
</head>
<body>
    <h1>Contact Form</h1>

    <!-- Display flash messages -->
    {% with messages = get_flashed_messages(with_categories=True) %}
        {% if messages %}
            <ul>
                {% for category, message in messages %}
                    <li class="{{ category }}">{{ message }}</li>
                {% endfor %}
            </ul>
        {% endif %}
    {% endwith %}

    <!-- Render form -->
    <form method="POST" action="{{ url_for('index') }}">
        {{ form.hidden_tag() }}  <!-- CSRF Token -->
        
        <div>
            {{ form.name.label }}  <!-- Label for Name -->
            {{ form.name(size=20) }}  <!-- Name input field -->
            {% if form.name.errors %}  <!-- Error handling for Name -->
                <ul>
                    {% for error in form.name.errors %}
                        <li style="color: red;">{{ error }}</li>
                    {% endfor %}
                </ul>
            {% endif %}
        </div>

        <div>
            {{ form.email.label }}  <!-- Label for Email -->
            {{ form.email(size=20) }}  <!-- Email input field -->
            {% if form.email.errors %}  <!-- Error handling for Email -->
                <ul>
                    {% for error in form.email.errors %}
                        <li style="color: red;">{{ error }}</li>
                    {% endfor %}
                </ul>
            {% endif %}
        </div>

        <div>
            {{ form.submit() }}  <!-- Submit button -->
        </div>
    </form>
</body>
</html>
```

### Explanation of `index.html`

- **`{{ form.hidden_tag() }}`**: Generates a CSRF token to protect the form against CSRF attacks.
- **`form.name.label`** and **`form.name()`**: Renders the label and input field for the `name` field.
- **`form.name.errors`**: Displays any validation errors for the `name` field, such as "This field is required."
- **Flash Messages**: If a form submission is successful, we use `flash()` in `app.py` to display a success message.

### Testing the Form

1. Run the Flask app:
   ```bash
   python app.py
   ```

2. Go to `http://127.0.0.1:5000/`.
3. Enter your name and email and submit the form:
   - If all fields are filled correctly, you should see a success message.
   - If any fields are empty or invalid, error messages will display next to the relevant fields.

This example demonstrates how to create, validate, and display a form in Flask using Flask-WTF, providing a basic foundation for handling user input in your Flask applications.