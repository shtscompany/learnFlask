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

- in Flask, the **`flash()`** function is used to send one-time messages from the server to the client. These messages are often used to give users feedback after a specific action, like form submission (e.g., "Form submitted successfully!") or login attempt (e.g., "Invalid username or password").

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

## Flask flash
In Flask, the `flash()` function is used to send one-time messages from the server to the client. These messages are often used to give users feedback after a specific action, like form submission (e.g., "Form submitted successfully!") or login attempt (e.g., "Invalid username or password").

Flash messages are stored in the user’s session and are removed automatically after being displayed once, so they’re ideal for providing temporary notifications to users.

### How `flash()` Works

1. **Flashing a Message**: You call `flash("Your message here")` in your route to add a message to the session.
2. **Displaying the Message**: In the template, you retrieve and display flashed messages using `get_flashed_messages()`.

### Example of Using `flash()` in Flask

#### Step 1: Flask Route with `flash()`

```python
from flask import Flask, render_template, flash, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

@app.route('/submit', methods=['POST', 'GET'])
def submit():
    # Example logic for form submission
    if request.method == 'POST':
        # Assuming form validation passed
        flash("Form submitted successfully!", "success")
        return redirect(url_for('submit'))
    return render_template('submit.html')
```

In this example:
- If the form is submitted successfully, we flash a success message and redirect back to the `/submit` route.

#### Step 2: Displaying Flash Messages in the Template

In the template file, `submit.html`, add the following code to display flash messages:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Form Submission</title>
</head>
<body>
    <h1>Submit Form</h1>

    <!-- Display flashed messages -->
    {% with messages = get_flashed_messages(with_categories=True) %}
        {% if messages %}
            <ul>
                {% for category, message in messages %}
                    <li class="{{ category }}">{{ message }}</li>
                {% endfor %}
            </ul>
        {% endif %}
    {% endwith %}

    <!-- Example form -->
    <form method="POST" action="{{ url_for('submit') }}">
        <input type="submit" value="Submit Form">
    </form>
</body>
</html>
```

- **`get_flashed_messages(with_categories=True)`**: Retrieves flashed messages. Setting `with_categories=True` allows you to add categories like `"success"` or `"error"` for styling purposes.
- **`category`**: You can apply conditional styling based on the message category (e.g., green for success, red for error).

### Example with Message Categories

When flashing a message, you can specify categories like `"success"`, `"error"`, `"info"`, etc., for customized styling in your template.

```python
flash("Successfully submitted the form!", "success")
flash("An error occurred. Please try again.", "error")
```

Then, in the HTML template, you can style messages differently based on their category:

```html
<ul>
    {% for category, message in messages %}
        <li class="{{ category }}">{{ message }}</li>
    {% endfor %}
</ul>
```

By using `flash()` and `get_flashed_messages()`, you can easily implement user feedback in your Flask application for a more interactive user experience.

## Flask redirect
In Flask, `redirect()` is used to redirect the user to a different route or URL. This is particularly useful after form submissions, logins, or any actions where you want to take the user to another page rather than having them refresh the current one (to avoid form re-submission, for example).

### Basic Syntax of `redirect()`

```python
from flask import redirect, url_for
```

- **`redirect(location)`**: Sends the user to the specified `location`, which can be an absolute URL or a relative URL.
- **`url_for()`**: Helps generate a URL to a specific route by its endpoint name, making redirection more dynamic and avoiding hardcoded URLs.

### Example Usage of `redirect()` in Flask

Let’s create a simple example where a form submission redirects to a "thank you" page.

#### Step 1: Define Routes in `app.py`

```python
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Example form handling
    if request.method == 'POST':
        # Perform form processing, validation, etc.
        # If everything is valid, redirect to the thank_you route
        return redirect(url_for('thank_you'))
    return redirect(url_for('index'))

@app.route('/thank_you')
def thank_you():
    return "<h1>Thank you for submitting the form!</h1>"

if __name__ == '__main__':
    app.run(debug=True)
```

- **`/submit` route**: After form submission, redirects the user to `/thank_you` if the form is processed successfully.
- **`url_for('thank_you')`**: Uses `url_for` to dynamically generate the URL for the `thank_you` route, which is helpful if your app’s URL structure changes.

#### Step 2: Create a Simple Form in `index.html`

Create a template named `index.html` to handle the form.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Submit Form</title>
</head>
<body>
    <h1>Submit Form</h1>
    <form method="POST" action="{{ url_for('submit') }}">
        <button type="submit">Submit</button>
    </form>
</body>
</html>
```

### Example Explanation

1. When the user visits the `/` route, they see the form in `index.html`.
2. Upon clicking "Submit," the form is submitted to the `/submit` route.
3. If the form is processed successfully, `redirect(url_for('thank_you'))` sends the user to the `/thank_you` route.
4. The user will then see the "Thank you" message on the new page.

### Common Use Cases for `redirect()`

1. **Redirecting After Form Submission**: Redirecting to avoid form re-submission on page refresh.
2. **Handling Unauthorized Access**: Redirect users to the login page if they attempt to access a restricted route.
3. **Redirecting After Login or Logout**: Redirect users to a welcome or dashboard page after logging in.

Using `redirect()` and `url_for()` together helps manage redirections efficiently and keeps URLs flexible in Flask applications.
