# WiFi Network Sharing Platform

A professional full-stack Django web application for managing and sharing WiFi networks across multiple devices with real-time monitoring and advanced security features.

## 🌟 Features

### Device Management
- Register multiple devices with MAC address tracking
- Real-time device status monitoring
- Support for various device types (Laptop, Phone, Tablet, Router, Hotspot, etc.)
- IP address tracking and device identification

### WiFi Network Management
- Create and manage multiple WiFi networks
- Support for various security protocols (Open, WEP, WPA, WPA2, WPA3)
- Configure frequency bands (2.4GHz, 5GHz, 6GHz)
- Channel management and signal strength monitoring
- Network activation/deactivation

### Network Sharing
- Share networks with specific users
- Granular permission levels:
  - **View Only**: Can see network details
  - **Can Connect**: Can connect to the network
  - **Can Manage**: Can manage network settings
- Expiring shares with automatic cleanup
- Share revocation at any time

### Network Invitations
- Send time-limited network invitations
- Automatic invitation expiration
- Invitation acceptance/rejection workflow
- Invite history tracking

### Real-time Monitoring
- Live connection tracking
- Connected device listing
- Connection quality monitoring
- Data usage tracking
- Last activity timestamps

### User Management
- Secure user registration and authentication
- User profile management
- First/last name tracking
- Email verification support

### Dashboard & Analytics
- Comprehensive dashboard with statistics
- Recent networks and devices overview
- Pending invitations display
- Active connection monitoring
- Quick navigation and actions

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Django 5.1+
- PostgreSQL (optional, SQLite for development)

### Installation

1. **Clone the repository**
```bash
cd sharing
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Apply migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Create a superuser**
```bash
python manage.py createsuperuser
```

5. **Run the development server**
```bash
python manage.py runserver
```

6. **Access the application**
- Website: http://localhost:8000
- Admin: http://localhost:8000/admin

## 📁 Project Structure

```
sharing/
├── filesharing/                 # Main Django app
│   ├── admin.py                # Admin configuration
│   ├── apps.py                 # App configuration
│   ├── models.py               # Database models
│   ├── views.py                # View handlers
│   ├── forms.py                # Form definitions
│   ├── urls.py                 # URL routing
│   ├── tests.py                # Unit tests
│   └── migrations/             # Database migrations
├── sharing/                     # Project settings
│   ├── settings.py             # Django settings
│   ├── urls.py                 # Main URL configuration
│   ├── asgi.py                 # ASGI configuration
│   └── wsgi.py                 # WSGI configuration
├── templates/                   # HTML templates
│   ├── base.html               # Base template
│   ├── home.html               # Landing page
│   ├── dashboard/              # Dashboard templates
│   ├── auth/                   # Authentication templates
│   ├── devices/                # Device management templates
│   ├── networks/               # Network management templates
│   ├── invitations/            # Invitation templates
│   ├── profile/                # User profile templates
│   └── search.html             # Search results
├── static/                      # Static files (CSS, JS, images)
├── manage.py                    # Django management script
├── db.sqlite3                   # SQLite database
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🗄️ Database Models

### Device
- UUID primary key
- User relationship (ForeignKey)
- Device name, type, MAC address
- IP address tracking
- Online/offline status
- Timestamps

### WiFiNetwork
- UUID primary key
- Owner relationship (User)
- Source device relationship
- SSID (network name)
- Password (encrypted)
- Security type (WPA2, WPA3, etc.)
- Frequency band and channel
- Signal strength
- Max devices capacity
- Active/inactive status
- Timestamps

### SharedNetwork
- UUID primary key
- Network relationship
- Device relationship
- Connection quality percentage
- Data usage tracking
- Connection timestamps

### NetworkShare
- UUID primary key
- Network relationship
- Shared with user relationship
- Permission levels
- Expiration date
- Active/inactive status

### NetworkInvitation
- UUID primary key
- Network relationship
- Invited user relationship
- Inviting user relationship
- Status (pending, accepted, rejected, expired)
- Expiration date
- Response timestamp

## 🔐 Security Features

1. **Authentication**
   - User registration with email verification
   - Secure password hashing with Django's built-in system
   - Session-based authentication

2. **Authorization**
   - Permission levels for network sharing
   - User-specific data isolation
   - Admin interface access control

3. **Data Protection**
   - Password fields are hashed
   - MAC addresses stored securely
   - CSRF protection on all forms
   - SQL injection prevention with ORM

4. **Network Security**
   - Support for multiple encryption standards
   - Password requirements for secured networks
   - Time-limited invitations

## 📊 URL Routes

### Authentication
- `GET /` - Landing page
- `GET /signup/` - Sign up form
- `POST /signup/` - Create new account
- `GET /login/` - Login form
- `POST /login/` - Authenticate user
- `GET /logout/` - Logout user

### Dashboard
- `GET /dashboard/` - Main dashboard

### Devices
- `GET /devices/` - List all devices
- `GET /devices/register/` - Register device form
- `POST /devices/register/` - Create new device
- `GET /devices/<pk>/` - Device details
- `GET /devices/<pk>/edit/` - Edit device form
- `POST /devices/<pk>/edit/` - Update device
- `POST /devices/<pk>/delete/` - Delete device

### Networks
- `GET /networks/` - List all networks
- `GET /networks/create/` - Create network form
- `POST /networks/create/` - Create new network
- `GET /networks/<pk>/` - Network details
- `GET /networks/<pk>/edit/` - Edit network form
- `POST /networks/<pk>/edit/` - Update network
- `POST /networks/<pk>/delete/` - Delete network
- `GET /networks/<pk>/share/` - Share network form
- `POST /networks/<pk>/share/` - Share with user
- `POST /networks/<pk>/share/<share_pk>/revoke/` - Revoke share
- `GET /networks/shared/` - Networks shared with user

### Invitations
- `GET /invitations/` - List pending invitations
- `GET /networks/<pk>/invite/` - Send invitation form
- `POST /networks/<pk>/invite/` - Send invitation
- `POST /invitations/<pk>/accept/` - Accept invitation
- `POST /invitations/<pk>/reject/` - Reject invitation

### User Profile
- `GET /profile/` - View profile
- `GET /profile/edit/` - Edit profile form
- `POST /profile/edit/` - Update profile

### API Endpoints
- `GET /api/network/<pk>/stats/` - Network statistics (JSON)
- `GET /api/device/<pk>/status/` - Device status (JSON)

### Search
- `GET /search/?q=query` - Search networks and devices

## 🎨 Frontend Technologies

- **Bootstrap 5.3** - Responsive grid system and components
- **Font Awesome 6.4** - Icon library
- **Custom CSS** - Professional styling with gradients and animations
- **Django Templates** - Server-side template rendering
- **Responsive Design** - Mobile-first approach

## 📝 Forms

### DeviceRegistrationForm
- Device name
- Device type selection
- MAC address (validated format)
- IP address (optional)

### WiFiNetworkForm
- Source device selection
- Network name (SSID)
- Password (for secured networks)
- Security type
- Frequency band
- Channel number
- Signal strength
- Maximum devices

### ShareNetworkForm
- User selection
- Permission level selection
- Expiration date (optional)

### NetworkInvitationForm
- User to invite
- Expiration date

### UserRegistrationForm
- Username
- Email
- Password
- Password confirmation

## 🔧 Configuration

### Settings.py
- Debug mode (False in production)
- Database configuration
- Installed apps
- Middleware
- Template configuration
- Static files configuration
- Media files configuration

### Environment Variables
Create a `.env` file in the project root:
```
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgresql://user:password@host:port/dbname
```

## 📦 Deployment

### Production Checklist
1. Set `DEBUG = False`
2. Set secure `SECRET_KEY`
3. Configure allowed hosts
4. Use PostgreSQL or MySQL
5. Set up HTTPS/SSL
6. Configure static files serving (Whitenoise or CDN)
7. Configure email backend
8. Set up proper logging
9. Use environment variables for sensitive data
10. Run migrations on production database

### Docker Deployment
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "sharing.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## 🧪 Testing

Run tests:
```bash
python manage.py test
```

Run with coverage:
```bash
coverage run --source='.' manage.py test
coverage report
```

## 📚 Admin Interface

Access the admin interface at `/admin/` with superuser credentials.

### Admin Features
- User management
- Device management with online status
- Network management with connection stats
- Share management
- Invitation management
- Filtered search and bulk actions

## 🐛 Troubleshooting

### Issue: Port already in use
```bash
python manage.py runserver 8001
```

### Issue: Database migration errors
```bash
python manage.py makemigrations
python manage.py migrate --fake-initial
```

### Issue: Static files not loading
```bash
python manage.py collectstatic
```

## 📖 API Documentation

### Get Network Stats
```
GET /api/network/<network_id>/stats/
Response: {
    "network_name": "MyWiFi",
    "is_active": true,
    "connected_devices": 5,
    "max_devices": 32,
    "total_data_used": 1024000,
    "signal_strength": -50,
    "channel": 6,
    "frequency_band": "2.4GHz"
}
```

### Get Device Status
```
GET /api/device/<device_id>/status/
Response: {
    "device_name": "My Laptop",
    "device_type": "Laptop",
    "is_online": true,
    "last_seen": "2024-01-15T10:30:00Z",
    "ip_address": "192.168.1.100",
    "mac_address": "00:1A:2B:3C:4D:5E"
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 💡 Future Enhancements

- Real-time WebSocket support
- QR code sharing for networks
- Network usage analytics dashboard
- Mobile app (iOS/Android)
- Advanced firewall rules
- Guest network creation
- Bandwidth throttling
- Automated backup and restore
- Integration with IoT devices
- Advanced encryption options

## 📞 Support

For support, email support@wifishare.com or open an issue on GitHub.

## ✨ Credits

Built with Django, Bootstrap, and Font Awesome.

---

**Made with ❤️ for WiFi Network Management**
