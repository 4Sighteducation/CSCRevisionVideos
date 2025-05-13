import os
from flask import Flask, request, jsonify, render_template
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
import datetime # Added for daily video selection

load_dotenv() # Load environment variables from .env file

app = Flask(__name__)

# Video data (could be moved to a separate file or DB in a larger app)
ALL_VIDEOS = [
    {"id": "zGDx41A", "title": "1. Managing your Physical Environment"},
    {"id": "avfERD2", "title": "2. Managing your Digital Environment"},
    {"id": "gf4fhoE", "title": "3. Will vs Skill - Strategic Study"},
    {"id": "oG2PRXN", "title": "4. Sticky Timetables"},
    {"id": "QFntkp8", "title": "5. 25min Sprints"},
    {"id": "qjmbeU8", "title": "6. Cog P vs Cog A"},
    {"id": "7WDUM16", "title": "7. High vs Low Utility"},
    {"id": "4vxb4Z2", "title": "8. Test your Future Self"},
    {"id": "p4ZN47c", "title": "9. Closed Book Notetaking"},
    {"id": "5AA3b27", "title": "10. Teach your imaginary Class"}
]

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

    # Select a daily featured video
    day_of_year = datetime.date.today().timetuple().tm_yday
    featured_video_index = (day_of_year - 1) % len(ALL_VIDEOS) # -1 for 0-based index
    featured_video = ALL_VIDEOS[featured_video_index]

    return render_template('index.html', message=message, error=error, featured_video=featured_video, all_videos=ALL_VIDEOS)

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

    # ---- TEMPORARY: Send simple email instead of template ----
    # subject = f"Simple Test from CSC App for {name}"
    # html_content = f"""
    #     <h1>Simple Test Email</h1>
    #     <p>This is a test to see if basic email sending works.</p>
    #     <p>Name: {name}</p>
    #     <p>Email: {email}</p>
    # """
    # message = Mail(
    #     from_email=SENDER_EMAIL,
    #     to_emails=[RECIPIENT_EMAIL],
    #     subject=subject,
    #     html_content=html_content
    # )
    # ---- END TEMPORARY ----

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Email sent via SendGrid template! Status Code: {response.status_code}")
        # Redirect back to index with success message
        # Need to pass featured_video again if redirecting to index, or make it available globally
        day_of_year = datetime.date.today().timetuple().tm_yday
        featured_video_index = (day_of_year - 1) % len(ALL_VIDEOS)
        featured_video = ALL_VIDEOS[featured_video_index]
        return render_template('index.html', message='Thank you! Your message has been sent successfully.', featured_video=featured_video, all_videos=ALL_VIDEOS)

    except Exception as e:
        print(f"Error sending email via SendGrid template: {e}")
        # Log the error details more robustly in a real application
        # Redirect back to index with error message
        day_of_year = datetime.date.today().timetuple().tm_yday
        featured_video_index = (day_of_year - 1) % len(ALL_VIDEOS)
        featured_video = ALL_VIDEOS[featured_video_index]
        return render_template('index.html', error='Sorry, there was an error sending your message. Please try again later.', featured_video=featured_video, all_videos=ALL_VIDEOS)

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