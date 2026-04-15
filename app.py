from flask import Flask, render_template, request,session, redirect, url_for    
import os
from models.eventFactory import EventFactory
from config.database import supabase_cf
from models.eventFactory import EventFactory
from services.event_strategy import PastEventStrategy, UpcomingEventStrategy, UpcomingEventStrategy
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
            return "You do not have permission to make edits in this portal.", 403
            
        return f(*args, **kwargs)
    return decorated

@app.route('/admin')
def admin():
    if 'email' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))
@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']
        
        try:
            db = supabase_cf()
            # 2. Attempt to fetch user
            result = db.table('users').select("*").eq('email', email).execute()
            user_data = result.data[0] if result.data else None
            
            print(f"DEBUG: Login attempt for {email}")

            if user_data:
                # 3. Verify hashed password
                match = check_password_hash(user_data['password_hash'], password)
                print(f"DEBUG: Password match result: {match}")
                
                if match:
                    session['email'] = user_data['email']
                    session['role'] = user_data['role']
                    session['name'] = user_data['name']
                    return redirect(url_for('dashboard'))

        except Exception as e:
            print(f"DEBUG CRITICAL: Database error: {e}")
            error = "Server error. Please try again later."
            return render_template('login.html', error=error)
        
        error = 'Invalid credentials. Please try again.'
            
    return render_template('login.html', error=error)

@app.route('/admin/dashboard')
@admin_required
def dashboard():
    if 'email' not in session:
        return redirect(url_for('login'))
    db = supabase_cf()
    response = db.table('events').select("*").order('id').execute()
    return render_template(
        'dashboard.html', 
        name=session['name'], 
        role=session['role'],
        events=response.data
    )
    

@app.route('/admin/add', methods=['POST'])
@admin_required
def add():
    db = supabase_cf()
    def parse_array(field_name):
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
        "perks": parse_array("perks"),

        "speaker": parse_array("speaker"), 
        "topic": clean("topic"),
        "theme": clean("theme"),
        "level": clean("level"),
        "industry": clean("industry"),
        "volunteers": clean("volunteers") 
    }
    
    cleanData = {k: v for k, v in eventData.items() if v is not None}
    
    db.table('events').insert(cleanData).execute()
    return redirect(url_for('dashboard'))

@app.route('/admin/delete/<int:event_id>')
@admin_required
def delete_event(event_id):
    db = supabase_cf()
    db.table('events').delete().eq('id', event_id).execute() 
    return redirect(url_for('dashboard'))

# resources
@app.route('/admin/resources')
@admin_required
def admin_resources():
    db = supabase_cf()
    response = db.table('resource').select("*").order('id', desc=True).execute()
    return render_template('adminResource.html', 
                           name=session['name'], 
                           role=session['role'], 
                           resources=response.data)


@app.route('/admin/resources/add', methods=['POST'])
@admin_required
def add_resource():
    db = supabase_cf()
    
    resource = {
        "name": request.form.get("name"),
        "link": request.form.get("link"),
        "description": request.form.get("description")
    }
    
    db.table('resource').insert(resource).execute()
    return redirect(url_for('adminResource'))


@app.route('/admin/resources/delete/<int:resource_id>')
@admin_required
def delete_resource(resource_id):
    db = supabase_cf()
    db.table('resource').delete().eq('id', resource_id).execute()
    return redirect(url_for('adminResource'))


@app.route('/')
def home():
    return render_template('home.html')

# @app.route('/events')
# def showEvents():
#     db = supabase_cf()
#     events = db.table('events').select('*').execute()

#     eventObj = []
#     for row in events.data:
#         new_event = EventFactory.createEvent(**row) 
#         eventObj.append(new_event)

#     strategy = UpcomingEventStrategy()
#     filtEvents = strategy.filter(row for row in eventObj)
#     return render_template('events.html', events=filtEvents)
@app.route('/events')
def showEvents():
    db = supabase_cf()
    raw_rows = db.table('events').select("*").execute().data
    
    for row in raw_rows:
        print(f"NAME: {row['name']} | endTime raw value: {row['endTime']} | eventType: {row['eventType']}")
    
    event_objects = [EventFactory.createEvent(**row) for row in raw_rows]
    strategy = UpcomingEventStrategy()
    upcoming = strategy.filter(event_objects)
    past_strat = PastEventStrategy()
    past = past_strat.filter(event_objects)

    return render_template('events.html', upcoming=upcoming, past=past)

@app.route('/rsvp/<int:event_id>', methods=['POST'])
def rsvp(event_id):
    db = supabase_cf()
    data = {
        "event_id": event_id,
        "user_name": request.form.get("name"),
        "user_email": request.form.get("email")
    }
    db.table('rsvp').insert(data).execute()
    return redirect(url_for('showEvents'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

    