from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
import json
from PIL import Image
import io
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///events.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# Context processor to provide 'now' variable to all templates
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='student')  # student, organizer, admin
    full_name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100))
    student_id = db.Column(db.String(20))
    phone = db.Column(db.String(15))
    profile_picture = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    events_created = db.relationship('Event', backref='creator', lazy=True)
    registrations = db.relationship('Registration', backref='user', lazy=True)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    event_type = db.Column(db.String(50), nullable=False)  # fest, seminar, webinar, workshop
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    venue = db.Column(db.String(200))
    max_participants = db.Column(db.Integer)
    current_participants = db.Column(db.Integer, default=0)
    registration_deadline = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    image_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    registrations = db.relationship('Registration', backref='event', lazy=True)

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='registered')  # registered, attended, cancelled
    attendance_confirmed = db.Column(db.Boolean, default=False)
    certificate_issued = db.Column(db.Boolean, default=False)
    certificate_url = db.Column(db.String(200))

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    notification_type = db.Column(db.String(50))  # event_update, registration, certificate

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    upcoming_events = Event.query.filter(
        Event.start_date >= datetime.utcnow(),
        Event.is_active == True
    ).order_by(Event.start_date).limit(6).all()
    
    featured_events = Event.query.filter(
        Event.is_active == True
    ).order_by(Event.created_at.desc()).limit(3).all()
    
    return render_template('index.html', 
                         upcoming_events=upcoming_events,
                         featured_events=featured_events)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        role = request.form['role']
        department = request.form.get('department', '')
        student_id = request.form.get('student_id', '')
        phone = request.form.get('phone', '')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'error')
            return redirect(url_for('register'))
        
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            full_name=full_name,
            role=role,
            department=department,
            student_id=student_id,
            phone=phone
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        total_events = Event.query.count()
        total_users = User.query.count()
        total_registrations = Registration.query.count()
        recent_events = Event.query.order_by(Event.created_at.desc()).limit(5).all()
        
        return render_template('admin_dashboard.html',
                             total_events=total_events,
                             total_users=total_users,
                             total_registrations=total_registrations,
                             recent_events=recent_events)
    
    elif current_user.role == 'organizer':
        my_events = Event.query.filter_by(creator_id=current_user.id).all()
        upcoming_events = Event.query.filter(
            Event.start_date >= datetime.utcnow(),
            Event.creator_id == current_user.id
        ).order_by(Event.start_date).all()
        
        return render_template('organizer_dashboard.html',
                             my_events=my_events,
                             upcoming_events=upcoming_events)
    
    else:  # student
        my_registrations = Registration.query.filter_by(user_id=current_user.id).all()
        upcoming_registered = [reg.event for reg in my_registrations 
                             if reg.event.start_date >= datetime.utcnow()]
        
        return render_template('student_dashboard.html',
                             my_registrations=my_registrations,
                             upcoming_registered=upcoming_registered)

@app.route('/events')
def events():
    page = request.args.get('page', 1, type=int)
    event_type = request.args.get('type', '')
    search = request.args.get('search', '')
    
    query = Event.query.filter(Event.is_active == True)
    
    if event_type:
        query = query.filter(Event.event_type == event_type)
    
    if search:
        query = query.filter(Event.title.contains(search) | Event.description.contains(search))
    
    events = query.order_by(Event.start_date).paginate(
        page=page, per_page=9, error_out=False)
    
    return render_template('events.html', events=events, event_type=event_type, search=search)

@app.route('/event/<int:event_id>')
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    is_registered = False
    if current_user.is_authenticated:
        is_registered = Registration.query.filter_by(
            user_id=current_user.id, event_id=event_id).first() is not None
    
    return render_template('event_detail.html', event=event, is_registered=is_registered)

@app.route('/event/register/<int:event_id>', methods=['POST'])
@login_required
def register_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    if event.registration_deadline and datetime.utcnow() > event.registration_deadline:
        flash('Registration deadline has passed!', 'error')
        return redirect(url_for('event_detail', event_id=event_id))
    
    if event.current_participants >= event.max_participants:
        flash('Event is full!', 'error')
        return redirect(url_for('event_detail', event_id=event_id))
    
    existing_registration = Registration.query.filter_by(
        user_id=current_user.id, event_id=event_id).first()
    
    if existing_registration:
        flash('You are already registered for this event!', 'error')
        return redirect(url_for('event_detail', event_id=event_id))
    
    registration = Registration(user_id=current_user.id, event_id=event_id)
    db.session.add(registration)
    
    event.current_participants += 1
    db.session.commit()
    
    # Create notification
    notification = Notification(
        user_id=current_user.id,
        title=f'Event Registration Confirmed',
        message=f'You have successfully registered for "{event.title}"',
        notification_type='registration'
    )
    db.session.add(notification)
    db.session.commit()
    
    flash('Registration successful!', 'success')
    return redirect(url_for('event_detail', event_id=event_id))

@app.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    if current_user.role not in ['organizer', 'admin']:
        flash('Only organizers can create events!', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        event_type = request.form['event_type']
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%dT%H:%M')
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%dT%H:%M')
        venue = request.form['venue']
        max_participants = int(request.form['max_participants'])
        registration_deadline = datetime.strptime(request.form['registration_deadline'], '%Y-%m-%dT%H:%M')
        
        event = Event(
            title=title,
            description=description,
            event_type=event_type,
            start_date=start_date,
            end_date=end_date,
            venue=venue,
            max_participants=max_participants,
            registration_deadline=registration_deadline,
            creator_id=current_user.id
        )
        
        db.session.add(event)
        db.session.commit()
        
        flash('Event created successfully!', 'success')
        return redirect(url_for('event_detail', event_id=event.id))
    
    return render_template('create_event.html')

@app.route('/manage_event/<int:event_id>')
@login_required
def manage_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    if current_user.role not in ['admin'] and event.creator_id != current_user.id:
        flash('You can only manage your own events!', 'error')
        return redirect(url_for('dashboard'))
    
    registrations = Registration.query.filter_by(event_id=event_id).all()
    
    return render_template('manage_event.html', event=event, registrations=registrations)

@app.route('/attendance/<int:registration_id>', methods=['POST'])
@login_required
def mark_attendance(registration_id):
    registration = Registration.query.get_or_404(registration_id)
    
    if current_user.role not in ['admin'] and registration.event.creator_id != current_user.id:
        flash('Unauthorized!', 'error')
        return redirect(url_for('dashboard'))
    
    registration.attendance_confirmed = True
    db.session.commit()
    
    flash('Attendance marked successfully!', 'success')
    return redirect(url_for('manage_event', event_id=registration.event_id))

@app.route('/issue_certificate/<int:registration_id>', methods=['POST'])
@login_required
def issue_certificate(registration_id):
    registration = Registration.query.get_or_404(registration_id)
    
    if current_user.role not in ['admin'] and registration.event.creator_id != current_user.id:
        flash('Unauthorized!', 'error')
        return redirect(url_for('dashboard'))
    
    if not registration.attendance_confirmed:
        flash('Cannot issue certificate without confirmed attendance!', 'error')
        return redirect(url_for('manage_event', event_id=registration.event_id))
    
    # Generate certificate (in a real app, you'd create a proper PDF)
    certificate_filename = f"certificate_{registration.id}_{uuid.uuid4().hex[:8]}.txt"
    certificate_path = os.path.join(app.config['UPLOAD_FOLDER'], certificate_filename)
    
    with open(certificate_path, 'w') as f:
        f.write(f"CERTIFICATE OF PARTICIPATION\n")
        f.write(f"Event: {registration.event.title}\n")
        f.write(f"Participant: {registration.user.full_name}\n")
        f.write(f"Date: {registration.event.start_date.strftime('%B %d, %Y')}\n")
        f.write(f"Issued on: {datetime.utcnow().strftime('%B %d, %Y')}\n")
    
    registration.certificate_issued = True
    registration.certificate_url = certificate_filename
    db.session.commit()
    
    # Create notification
    notification = Notification(
        user_id=registration.user_id,
        title=f'Certificate Issued',
        message=f'Your certificate for "{registration.event.title}" has been issued!',
        notification_type='certificate'
    )
    db.session.add(notification)
    db.session.commit()
    
    flash('Certificate issued successfully!', 'success')
    return redirect(url_for('manage_event', event_id=registration.event_id))

@app.route('/download_certificate/<int:registration_id>')
@login_required
def download_certificate(registration_id):
    registration = Registration.query.get_or_404(registration_id)
    
    if registration.user_id != current_user.id:
        flash('Unauthorized!', 'error')
        return redirect(url_for('dashboard'))
    
    if not registration.certificate_issued:
        flash('Certificate not yet issued!', 'error')
        return redirect(url_for('dashboard'))
    
    certificate_path = os.path.join(app.config['UPLOAD_FOLDER'], registration.certificate_url)
    
    if os.path.exists(certificate_path):
        return send_file(certificate_path, as_attachment=True)
    else:
        flash('Certificate file not found!', 'error')
        return redirect(url_for('dashboard'))

@app.route('/notifications')
@login_required
def notifications():
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
    return render_template('notifications.html', notifications=notifications)

@app.route('/mark_notification_read/<int:notification_id>', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    
    if notification.user_id != current_user.id:
        flash('Unauthorized!', 'error')
        return redirect(url_for('notifications'))
    
    notification.is_read = True
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        current_user.full_name = request.form['full_name']
        current_user.email = request.form['email']
        current_user.department = request.form.get('department', '')
        current_user.phone = request.form.get('phone', '')
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('edit_profile.html')

# API Routes for AJAX
@app.route('/api/events')
def api_events():
    events = Event.query.filter(Event.is_active == True).all()
    return jsonify([{
        'id': event.id,
        'title': event.title,
        'start_date': event.start_date.isoformat(),
        'end_date': event.end_date.isoformat(),
        'event_type': event.event_type,
        'venue': event.venue
    } for event in events])

@app.route('/api/event_stats/<int:event_id>')
@login_required
def api_event_stats(event_id):
    event = Event.query.get_or_404(event_id)
    
    if current_user.role not in ['admin'] and event.creator_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    registrations = Registration.query.filter_by(event_id=event_id).all()
    attended = sum(1 for reg in registrations if reg.attendance_confirmed)
    certificates_issued = sum(1 for reg in registrations if reg.certificate_issued)
    
    return jsonify({
        'total_registrations': len(registrations),
        'attended': attended,
        'certificates_issued': certificates_issued,
        'attendance_rate': (attended / len(registrations) * 100) if registrations else 0
    })

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
