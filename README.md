# EventHub - College Event Management System 🎯

A comprehensive, modern web application for managing college events, fests, seminars, and webinars. Built with Python Flask and featuring a beautiful, responsive UI designed to win competitions.

## ✨ Features

### 🎉 Core Functionality
- **Event Management**: Create, edit, and manage various types of events
- **User Registration**: Student and organizer role-based access
- **Event Registration**: Easy participant registration with capacity management
- **Attendance Tracking**: Mark and confirm participant attendance
- **Digital Certificates**: Generate and issue professional PDF/HTML certificates automatically
- **Smart Notifications**: Real-time updates and reminders

### 🎨 User Experience
- **Modern UI/UX**: Beautiful, responsive design with Bootstrap 5
- **Role-Based Dashboards**: Customized views for students, organizers, and admins
- **Search & Filtering**: Advanced event discovery with multiple criteria
- **Mobile Responsive**: Works perfectly on all devices
- **Real-time Updates**: Live statistics and progress tracking

### 🔐 Security & Management
- **User Authentication**: Secure login with password hashing
- **Role Management**: Student, Organizer, and Admin roles
- **Data Validation**: Comprehensive form validation and security
- **File Management**: Secure file uploads and certificate generation

## 🚀 Technology Stack

- **Backend**: Python 3.11, Flask 2.3.3
- **Database**: SQLAlchemy with SQLite (local) / PostgreSQL (production)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Authentication**: Flask-Login with bcrypt
- **Icons**: Font Awesome 6.4.0
- **Deployment**: Heroku-ready with Gunicorn

## 📋 Requirements

- Python 3.11+
- Flask 2.3.3
- Flask-SQLAlchemy 3.0.5
- Flask-Login 0.6.3
- Flask-WTF 1.1.1
- WTForms 3.0.1
- Pillow 10.0.1
- python-dotenv 1.0.0
- gunicorn 21.2.0
- email-validator 2.0.0
- bcrypt 4.0.1
- weasyprint 60.2 (for PDF certificate generation)
- reportlab 4.0.4 (alternative PDF generation)

## 🛠️ Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/college_event_system.git
   cd college_event_system
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**
   ```bash
   export FLASK_APP=app.py
   export FLASK_ENV=development
   export SECRET_KEY=your-secret-key-here
   ```

5. **Initialize database**
   ```bash
   python app.py
   ```

6. **Run the application**
   ```bash
   flask run
   ```

The application will be available at `http://localhost:5000`

### Certificate System Setup

The system includes a professional certificate generation system that can create beautiful PDF certificates:

1. **PDF Generation (Recommended)**
   - Uses WeasyPrint for high-quality PDF generation
   - Professional certificate template with custom styling
   - Automatic certificate numbering and validation

2. **Fallback HTML Certificates**
   - If WeasyPrint is not available, generates HTML certificates
   - Can be printed or saved as PDF using browser print function
   - Maintains professional appearance

3. **System Dependencies**
   - **macOS**: `brew install cairo pango gdk-pixbuf libffi`
   - **Ubuntu/Debian**: `sudo apt-get install build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info`
   - **Windows**: Install GTK+ runtime environment

4. **Test Certificate Generation**
   ```bash
   python test_certificate.py
   ```

### Heroku Deployment

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew install heroku/brew/heroku
   
   # Windows
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

4. **Set environment variables**
   ```bash
   heroku config:set SECRET_KEY=your-production-secret-key
   heroku config:set FLASK_ENV=production
   ```

5. **Deploy**
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push heroku main
   ```

6. **Open the app**
   ```bash
   heroku open
   ```

## 🎯 Usage Guide

### For Students
1. **Register/Login**: Create an account with student role
2. **Browse Events**: Search and filter available events
3. **Register for Events**: Join events of interest
4. **Track Progress**: Monitor registrations and attendance
5. **Download Certificates**: Get certificates for completed events

### For Organizers
1. **Create Events**: Set up new events with detailed information
2. **Manage Registrations**: Track participant sign-ups
3. **Mark Attendance**: Confirm participant presence
4. **Issue Certificates**: Generate certificates for attendees
5. **Analytics**: View event statistics and reports

### For Admins
1. **System Overview**: Monitor overall system health
2. **User Management**: Oversee all users and roles
3. **Event Oversight**: Manage all events in the system
4. **Reports**: Generate comprehensive system reports

## 🏗️ Project Structure

```
college_event_system/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Procfile             # Heroku deployment configuration
├── runtime.txt          # Python version specification
├── templates/           # HTML templates
│   ├── base.html       # Base template with navigation
│   ├── index.html      # Landing page
│   ├── login.html      # Login form
│   ├── register.html   # Registration form
│   ├── dashboard/      # Dashboard templates
│   ├── events/         # Event-related templates
│   └── profile/        # User profile templates
├── static/             # Static assets
│   ├── css/           # Custom CSS styles
│   ├── js/            # JavaScript files
│   └── images/        # Image assets
└── uploads/           # File uploads (certificates)
```

## 🔧 Configuration

### Environment Variables
- `SECRET_KEY`: Flask secret key for sessions
- `DATABASE_URL`: Database connection string
- `FLASK_ENV`: Environment (development/production)
- `UPLOAD_FOLDER`: Path for file uploads

### Database Models
- **User**: User accounts with role-based access
- **Event**: Event information and details
- **Registration**: Event participation records
- **Notification**: User notification system

## 🚀 Performance Features

- **Responsive Design**: Mobile-first approach
- **Optimized Queries**: Efficient database operations
- **Caching**: Smart caching for better performance
- **Lazy Loading**: Progressive content loading
- **CDN Integration**: Fast asset delivery

## 🎨 UI/UX Highlights

- **Modern Design**: Clean, professional appearance
- **Color Scheme**: Consistent brand colors and themes
- **Typography**: Readable fonts with proper hierarchy
- **Icons**: Meaningful iconography throughout
- **Animations**: Subtle hover effects and transitions
- **Accessibility**: WCAG compliant design

## 🔒 Security Features

- **Password Hashing**: Bcrypt encryption
- **CSRF Protection**: Form security
- **Input Validation**: Comprehensive data validation
- **Session Management**: Secure user sessions
- **Role-Based Access**: Controlled feature access

## 📱 Mobile Optimization

- **Responsive Grid**: Bootstrap 5 responsive system
- **Touch-Friendly**: Optimized for mobile devices
- **Fast Loading**: Optimized for mobile networks
- **Progressive Web App**: PWA-ready features

## 🧪 Testing

### Manual Testing
1. **User Registration**: Test all user roles
2. **Event Creation**: Create various event types
3. **Registration Flow**: Complete event registration
4. **Attendance Marking**: Test attendance system
5. **Certificate Generation**: Verify certificate creation

### Automated Testing
```bash
# Run tests (when implemented)
python -m pytest tests/

# Coverage report
python -m pytest --cov=app tests/
```

## 🚀 Deployment Checklist

- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] Static files collected
- [ ] SSL certificate configured
- [ ] Error monitoring set up
- [ ] Performance monitoring enabled
- [ ] Backup strategy implemented

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏆 Competition Ready Features

- **Professional UI/UX**: Competition-winning design
- **Comprehensive Functionality**: Full event management lifecycle
- **Scalable Architecture**: Ready for production use
- **Modern Technologies**: Latest web development stack
- **Documentation**: Complete setup and usage guides
- **Deployment Ready**: Heroku deployment included

## 📞 Support

For support and questions:
- **Email**: support@eventhub.edu
- **Documentation**: [Project Wiki](wiki-link)
- **Issues**: [GitHub Issues](issues-link)

## 🎉 Acknowledgments

- Flask community for the excellent framework
- Bootstrap team for the responsive CSS framework
- Font Awesome for the beautiful icons
- All contributors and testers

---

**Built with ❤️ for college event management excellence**
