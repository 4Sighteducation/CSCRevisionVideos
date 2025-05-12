import os
from flask import Flask, request, jsonify, render_template
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

app = Flask(__name__)

# Ensure environment variables are set
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')
SENDER_EMAIL = os.getenv('SENDER_EMAIL', RECIPIENT_EMAIL) # Use recipient as sender if not specified
SENDGRID_TEMPLATE_ID = os.getenv('SENDGRID_TEMPLATE_ID') # Added Template ID

if not SENDGRID_API_KEY:
    print("Error: SENDGRID_API_KEY not found in environment variables.")
    # Depending on deployment, might want to raise an error or exit
if not RECIPIENT_EMAIL:
    print("Error: RECIPIENT_EMAIL not found in environment variables.")
    # Depending on deployment, might want to raise an error or exit
if not SENDGRID_TEMPLATE_ID: # Added check for Template ID
    print("Error: SENDGRID_TEMPLATE_ID not found in environment variables.")

@app.route('/')
def index():
    # Pass message/error from submit_form result if available
    message = request.args.get('message')
    error = request.args.get('error')
    return render_template('index.html', message=message, error=error)

@app.route('/submit', methods=['POST'])
def submit_form():
    # Check essential configurations on each request
    if not SENDGRID_API_KEY or not RECIPIENT_EMAIL or not SENDER_EMAIL or not SENDGRID_TEMPLATE_ID:
        print("Server configuration error: Missing SendGrid API Key, Recipient, Sender or Template ID.")
        # Redirect back to form with error message
        return render_template('index.html', error='Sorry, the server is not configured correctly to send emails.')
        # return jsonify({'status': 'error', 'message': 'Server configuration error.'}), 500

    name = request.form.get('name')
    email = request.form.get('email')
    school = request.form.get('school', 'Not Provided') # Optional field
    message_body = request.form.get('message')

    if not name or not email or not message_body:
        # return jsonify({'status': 'error', 'message': 'Missing required form fields.'}), 400
        return render_template('index.html', error='Please fill in all required fields (Name, Email, Message).')


    # Data to be passed to the SendGrid template
    template_data = {
        'name': name,
        'email': email,
        'school': school,
        'message_body': message_body
        # Ensure these keys match the {{variables}} in your SendGrid template
    }

    # Construct the email using the Template ID
    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=[RECIPIENT_EMAIL] # Pass recipient email as a list
        # Subject is set in the SendGrid template itself
    )
    # Add template ID and dynamic data
    message.template_id = SENDGRID_TEMPLATE_ID
    message.dynamic_template_data = template_data

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Email sent via SendGrid template! Status Code: {response.status_code}")
        # Redirect back to index with success message
        return render_template('index.html', message='Thank you! Your message has been sent successfully.')

    except Exception as e:
        print(f"Error sending email via SendGrid template: {e}")
        # Log the error details more robustly in a real application
        # Redirect back to index with error message
        return render_template('index.html', error='Sorry, there was an error sending your message. Please try again later.')

# Example Thank You / Error routes (if redirecting)
# @app.route('/thank-you')
# def thank_you():
#     return "<h1>Thank You!</h1><p>Your message has been sent successfully.</p><a href='/'>Back to Home</a>"
#
# @app.route('/error-page')
# def error_page():
#      return "<h1>Error</h1><p>Sorry, there was an error sending your message.</p><a href='/'>Back to Home</a>"

if __name__ == '__main__':
    # Port 5000 is standard for Flask dev server
    # Use 0.0.0.0 to make it accessible on the network
    app.run(host='0.0.0.0', port=5000, debug=True) # Turn debug=False for production 