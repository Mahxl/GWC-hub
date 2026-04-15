from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/events')
def events():
    return render_template("events.html")

@app.route('/techHer')
def techher():
    return render_template("techHer.html")

@app.route('/resources')
def resources():
    return render_template("resources.html")

@app.route('/newsletter')
def newsletter():
    return render_template("newsletter.html")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        sender_email = request.form.get('email')
        message = request.form.get('message')

        try:
            gmail_user = os.environ.get("GWC_EMAIL")
            gmail_password = os.environ.get("GWC_APP_PASSWORD")
            recipient_email = "girlswhocodeumdearborn@gmail.com"

            msg = MIMEMultipart()
            msg['From'] = gmail_user
            msg['To'] = recipient_email
            msg['Subject'] = f"New Contact Form Message from {name}"

            body = f"""
You received a new message from the Girls Who Code website contact form.

Name: {name}
Email: {sender_email}

Message:
{message}
"""
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(gmail_user, gmail_password)
            server.send_message(msg)
            server.quit()

            flash("Your message was sent successfully!")
            return redirect(url_for('contact'))

        except Exception as e:
            print("Email error:", e)
            flash("Something went wrong. Please try again.")
            return redirect(url_for('contact'))

    return render_template("contact.html")

if __name__ == '__main__':
    app.run(debug=True)