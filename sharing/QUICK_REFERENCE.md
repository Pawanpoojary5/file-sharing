# Quick Reference Guide - WiFi Network Sharing Platform

## 🚀 One-Minute Setup

```bash
cd sharing
# Windows:
setup.bat
# Linux/Mac:
./setup.sh

# Then:
python manage.py runserver
# Visit: http://localhost:8000
```

## 🔗 Key URLs

| Page | URL | Purpose |
|------|-----|---------|
| Home | `/` | Landing page |
| Dashboard | `/dashboard/` | Main dashboard |
| Devices | `/devices/` | List all devices |
| Register Device | `/devices/register/` | Add new device |
| Networks | `/networks/` | List all networks |
| Create Network | `/networks/create/` | Add new network |
| Invitations | `/invitations/` | View pending invites |
| Profile | `/profile/` | User account |
| Login | `/login/` | Sign in |
| Signup | `/signup/` | Create account |
| Admin | `/admin/` | Admin panel |

## 📁 Important Files

```
models.py          - Database models (Device, WiFiNetwork, etc.)
views.py           - View functions (35+)
forms.py           - Form classes (8)
urls.py            - URL routing (35+)
admin.py           - Admin configuration
templates/base.html - Master template
requirements.txt   - Python dependencies
settings.py        - Django configuration
```

## 🎯 Common Tasks

### Register a Device
1. Click "Devices" → "Register New Device"
2. Enter device name, type, and MAC address
3. Click "Register Device"

### Create a WiFi Network
1. Click "Networks" → "Create Network"
2. Select source device
3. Enter network details (name, password, security type, etc.)
4. Click "Create Network"

### Share Network with Friend
1. Go to network details
2. Click "Share"
3. Select user and permission level
4. Click "Share Network"

### Send Network Invitation
1. Go to network details
2. Click "Send Invitation"
3. Select user and expiration date
4. Click "Send Invitation"

### Accept Network Invitation
1. Go to "Invitations" menu
2. Click "Accept" on desired invitation
3. Network appears in shared networks

## 🔧 Useful Commands

```bash
# Start server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Reset database (dev only)
rm db.sqlite3
python manage.py migrate

# Run tests
python manage.py test

# Collect static files
python manage.py collectstatic

# Django shell
python manage.py shell
```

## 📊 Model Fields Reference

### Device
- `device_name` - User-friendly name
- `device_type` - laptop, phone, tablet, router, hotspot, other
- `mac_address` - Hardware address (XX:XX:XX:XX:XX:XX)
- `ip_address` - Network IP address
- `is_online` - Connection status

### WiFiNetwork
- `network_name` - SSID
- `password` - Network password
- `security_type` - open, wep, wpa, wpa2, wpa3
- `frequency_band` - 2.4GHz, 5GHz, 6GHz
- `channel` - 1-165
- `max_devices` - Maximum connections

### NetworkShare
- `permission_level` - view, connect, manage
- `expires_at` - Optional expiration date
- `is_active` - Active/inactive status

## 🔐 Security Notes

- Store sensitive data in `.env` file
- Never commit `.env` to git
- Use strong passwords (8+ characters)
- Enable HTTPS in production
- Keep dependencies updated
- Use environment variables for secrets

## 🎨 Styling Guide

- **Primary Color**: #4f46e5 (Indigo)
- **Secondary Color**: #06b6d4 (Cyan)
- **Success**: #10b981 (Green)
- **Danger**: #ef4444 (Red)
- **Warning**: #f59e0b (Amber)

## 📱 Responsive Breakpoints

- **Mobile**: < 576px
- **Tablet**: 576px - 768px
- **Desktop**: 768px - 1200px
- **Large**: > 1200px

## 🐛 Troubleshooting

### Port 8000 in use
```bash
python manage.py runserver 8001
```

### Migrations not applying
```bash
python manage.py migrate --fake-initial
```

### Static files not loading
```bash
python manage.py collectstatic --noinput
```

### Can't login to admin
```bash
python manage.py createsuperuser
```

### Database locked
```bash
rm db.sqlite3
python manage.py migrate
```

## 📈 Performance Tips

1. Use indexes on frequently searched fields
2. Cache database queries
3. Paginate large result sets
4. Use select_related() for ForeignKeys
5. Use prefetch_related() for reverse relationships
6. Monitor query performance

## 🔗 Related Files

- **Requirements**: `requirements.txt`
- **Setup Guide**: `SETUP_GUIDE.md`
- **Full Documentation**: `README.md`
- **Project Summary**: `PROJECT_SUMMARY.md`

## 🎓 Learning Resources

- Django Docs: https://docs.djangoproject.com/
- Bootstrap Docs: https://getbootstrap.com/docs/5.3/
- Font Awesome: https://fontawesome.com/
- Django REST Framework: https://www.django-rest-framework.org/

## ✨ What's Included

- ✅ 5 Database Models
- ✅ 35+ Views
- ✅ 8 Form Classes
- ✅ 15+ Templates
- ✅ Professional Admin
- ✅ Mobile Responsive
- ✅ Complete Documentation
- ✅ One-Click Setup

## 🚀 Next Steps

1. Run setup script
2. Create account
3. Register device
4. Create network
5. Share with friends
6. Monitor in real-time

---

**Need Help?** See SETUP_GUIDE.md or README.md

**Ready to Deploy?** See README.md Production Checklist
