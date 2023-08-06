import os
from dotenv import load_dotenv
import requests
import smtplib
from email.message import EmailMessage
from flask import Flask, render_template, request

app = Flask(__name__)

res = requests.get("https://api.npoint.io/2283eae76d2033d9a728")
all_blogposts = res.json()


def send_email(form_content):
    load_dotenv()
    email_password = os.environ.get("EMAIL_PASSWORD")
    email_sender = os.environ.get("EMAIL_SENDER")
    email_recipient = os.environ.get("EMAIL_RECIPIENT")
    smtp_server = os.environ.get("SMTP_SERVER")
    port = os.environ.get("PORT")

    # Format email
    email = EmailMessage()
    body = f"Name: {form_content['name']}\n" \
           f"Email: {form_content['email']}\n" \
           f"Phone: {form_content['phone']}\n" \
           f"Message:\n\n{form_content['message']}"
    email.set_content(body)
    #email.set_content(message, subtype='html')
    email["From"] = f"{form_content['name']} via Blog Contact Form"
    email["To"] = email_recipient
    email["Subject"] = "Message from Blog Contact Form"

    with smtplib.SMTP(host=smtp_server, port=port) as connection:
        connection.starttls()
        connection.login(user=email_sender, password=email_password)
        connection.send_message(email)
        connection.close()

@app.route("/")
def home():
    return render_template("index.html", posts = all_blogposts)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/message-sent", methods=["POST"])
def receive_contact_data():
    send_email(request.form)
    return render_template("contact.html", message_sent = True)

@app.route("/<int:post_id>")
def display_post(post_id):
    return render_template("post.html", post = all_blogposts[post_id - 1])
if __name__ == "__main__":
    app.run(debug=True)
