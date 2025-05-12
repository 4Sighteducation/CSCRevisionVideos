# CSC Revision Video Webpage

This project is a single webpage designed to host revision videos from the Central South Consortium, powered by VESPA Academy. It includes a contact form that sends an email notification for new inquiries using Flask and SendGrid.

## Features

- Displays logos for CSC and VESPA Academy.
- Lists 10 embedded revision videos.
- Provides marketing information for VESPA Academy.
- Includes a contact form (Name, Email, School/Organization, Message).
- Sends form submissions to a designated email address via SendGrid.

## Project Structure

```
/
|-- app.py               # Flask application for backend and email sending
|-- index.html           # Main webpage content
|-- style.css            # Custom CSS styles
|-- requirements.txt     # Python dependencies
|-- .env                 # Environment variables (SendGrid API key, email settings) - YOU MUST CREATE THIS
|-- .gitignore           # Specifies intentionally untracked files that Git should ignore
|-- README.md            # This file
|-- templates/
    |-- index.html       # (app.py will look for index.html here by default)
```

**Note:** For Flask to correctly find `index.html`, it should be placed inside a `templates` folder in the root directory of the project. The `app.py` script is configured to look for `render_template('index.html')` which expects this structure.

## Setup and Running the Project

### 1. Prerequisites

- Python 3.x installed.
- A SendGrid account and API Key.
- A verified sender email address in SendGrid.

### 2. Clone the Repository (if applicable)

If this project is in a Git repository, clone it:
```bash
git clone <repository-url>
cd <repository-name>
```

### 3. Create a Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.

```bash
# Create a virtual environment (e.g., named 'venv')
python -m venv venv

# Activate the virtual environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a file named `.env` in the root of your project directory. Copy the following content into it and replace the placeholder values:

```.env
# Environment variables for CSC Revision Page

# Your SendGrid API Key (Keep this secret!)
SENDGRID_API_KEY='YOUR_SENDGRID_API_KEY_HERE'

# Email address where the contact form submissions will be sent
RECIPIENT_EMAIL='admin@vespa.academy'

# Verified sender email address in your SendGrid account
# This email will appear as the "from" address.
# For example: SENDER_EMAIL='noreply@yourdomain.com' or SENDER_EMAIL='admin@vespa.academy' (if verified)
SENDER_EMAIL='admin@vespa.academy'
```

**Important:**
- Replace `'YOUR_SENDGRID_API_KEY_HERE'` with your actual SendGrid API key.
- Ensure `SENDER_EMAIL` is an email address you have verified as a sender in your SendGrid account.
- The `RECIPIENT_EMAIL` is where the inquiries will be sent.

### 6. Create the `templates` folder

Flask, by default, looks for HTML templates in a folder named `templates`. Create this folder in the root of your project and move the `index.html` file into it.

```bash
mkdir templates
# On Windows (PowerShell/cmd):
# move index.html templates\
# On macOS/Linux:
# mv index.html templates/
```
Your project structure should now look like:
```
/
|-- app.py
|-- style.css
|-- requirements.txt
|-- .env
|-- .gitignore
|-- README.md
|-- templates/
    |-- index.html
```

### 7. Run the Flask Application

```bash
python app.py
```

The application will typically start on `http://127.0.0.1:5000/` or `http://0.0.0.0:5000/`.
Open this URL in your web browser to see the webpage.

### 8. Testing the Form

Fill out the contact form and submit it. Check the email address specified in `RECIPIENT_EMAIL` (admin@vespa.academy) for the new message. Also, check the console output of the `app.py` script for any logs or errors.

## Stopping the Application

Press `Ctrl+C` in the terminal where the Flask app is running.

## Deactivating the Virtual Environment (Optional)

When you are done working on the project:
```bash
deactivate
``` 