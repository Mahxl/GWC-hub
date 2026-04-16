from flask import Flask, render_template, request, session, redirect, url_for    
import os
from models.eventFactory import EventFactory
from config.database import supabase_cf
from services.event_strategy import PastEventStrategy, UpcomingEventStrategy
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'gwc_dearborn2026'  

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'email' not in session:
            return redirect(url_for('login'))
        if session.get('role') not in ['admin', 'superAdmin']:
            return "Unauthorized", 403
        return f(*args, **kwargs)
    return decorated

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/admin', methods=['GET', 'POST'])
def login():
    if request.method == 'GET' and 'email' in session:
        return redirect(url_for('dashboard'))

    error = None
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']
        
        try:
            db = supabase_cf()
            result = db.table('users').select("*").eq('email', email).execute()
            user_data = result.data[0] if result.data else None
            
            if user_data and check_password_hash(user_data['password_hash'], password):
                session['email'] = user_data['email']
                session['role'] = user_data['role']
                session['name'] = user_data['name']
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid credentials.'

        except Exception as e:
            print(f"DB Error: {e}")
            error = "Server error."
    
    return render_template('admin/login.html', error=error)


@app.route('/admin/dashboard')
@admin_required
def dashboard():
    db = supabase_cf()
    response = db.table('events').select("*").order('id').execute()

    return render_template('admin/dashboard.html', 
                           name=session['name'], 
                           role=session['role'], 
                           events=response.data)
@app.route('/admin/resources')
@admin_required
def admin_resources():
    db = supabase_cf()
    response = db.table('resource').select("*").order('id', desc=True).execute()
    return render_template('admin/adminResource.html', 
                           name=session['name'], 
                           role=session['role'], 
                           resources=response.data)


@app.route('/admin/add', methods=['POST'])
@admin_required
def add():
    db = supabase_cf()
    def parse(field_name):
        val = request.form.get(field_name)
        if not val or val.strip() == "":
            return [] 
        return [item.strip() for item in val.split(',')]

    def clean(field_name):
        val = request.form.get(field_name)
        if not val or val.strip() == "":
            return None
        return val.strip()


    eventData = {
        "name": clean("name"),
        "eventType": clean("eventType"),
        "startTime": clean("startTime"),
        "endTime": clean("endTime"),
        "location": clean("location"),
        "description": clean("description"),
        "flyer_img": clean("flyer_img"),
        "perks": parse("perks"),  
        
        #these are the custom per evnt type in factory
        "speaker": parse("speaker"), 
        "topic": clean("topic"),
        "theme": clean("theme"),
        "level": clean("level"),
        "industry": clean("industry"),
        "volunteers": clean("volunteers") 
    }
    
    cleanData = {k: v for k, v in eventData.items() if v is not None}
    
    try:
        db.table('events').insert(cleanData).execute()
        print(f"SUCCESS: Event '{cleanData.get('name')}' published.")
    except Exception as e:
        print(f"ERROR: Could not save to Supabase: {e}")
        return "Database Error", 500
    return redirect(url_for('dashboard'))

@app.route('/admin/delete/<int:event_id>')
@admin_required
def delete_event(event_id):
    db = supabase_cf()
    db.table('events').delete().eq('id', event_id).execute() 
    return redirect(url_for('dashboard'))

@app.route('/admin/resources/add', methods=['POST'])
@admin_required
def add_resource():
    return redirect(url_for('admin_resources'))

@app.route('/admin/resources/delete/<int:resource_id>')
@admin_required
def delete_resource(resource_id):
    db = supabase_cf()
    db.table('resource').delete().eq('id', resource_id).execute()
    return redirect(url_for('admin_resources'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/events')
def showEvents():
    db = supabase_cf()
    raw_rows = db.table('events').select("*").execute().data
    event_objects = [EventFactory.createEvent(**row) for row in raw_rows]
    upcoming = UpcomingEventStrategy().filter(event_objects)
    past = PastEventStrategy().filter(event_objects)
    return render_template('events.html', upcoming=upcoming, past=past)

@app.route('/techHer')
def techher():
    return render_template('techHer.html')

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
    app.run(debug=True, host='0.0.0.0', port=5001)
