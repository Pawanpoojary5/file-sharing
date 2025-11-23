# WiFi Network Sharing Platform - Setup Guide

## Initial Setup Instructions

### Step 1: Install Python Dependencies

```bash
cd sharing
pip install -r requirements.txt
```

### Step 2: Create Database Migrations

Since this is a new project with new models, create and apply migrations:

```bash
# Create migrations for all models
python manage.py makemigrations

# Apply migrations to create database tables
python manage.py migrate
```

You should see output like:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, filesharing
Running migrations:
  Applying filesharing.0001_initial... OK
  ...
```

### Step 3: Create Superuser Account

Create an admin account to access the Django admin interface:

```bash
python manage.py createsuperuser
```

You'll be prompted to enter:
- Username
- Email address
- Password
- Confirm password

Example:
```
Username: admin
Email address: admin@example.com
Password: 
Superuser created successfully.
```

### Step 4: Run Development Server

Start the Django development server:

```bash
python manage.py runserver
```

The server will start at `http://localhost:8000`

```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Step 5: Access the Application

#### Main Website
- **Home Page**: http://localhost:8000/
- **Dashboard**: http://localhost:8000/dashboard/
- **Login**: http://localhost:8000/login/
- **Sign Up**: http://localhost:8000/signup/

#### Admin Interface
- **Admin Panel**: http://localhost:8000/admin/
- **Username**: Use the superuser credentials you created
- **Password**: Use the superuser password you created

## First Time User Guide

### 1. Create an Account
- Go to http://localhost:8000/signup/
- Fill in username, email, and password
- Click "Create Account"

### 2. Register Your First Device
- Click "Devices" in the navigation menu
- Click "Register New Device"
- Fill in:
  - Device Name (e.g., "My Laptop")
  - Device Type (select from dropdown)
  - MAC Address (see guide on how to find it)
  - IP Address (optional)
- Click "Register Device"

#### Finding MAC Address:
**Windows:**
```bash
ipconfig /all
# Look for "Physical Address"
```

**Mac/Linux:**
```bash
ifconfig
# Look for "HWaddr" or "ether"
```

**iPhone/iPad:**
- Settings → General → About → WiFi Address

**Android:**
- Settings → About phone → Status → WiFi MAC Address

### 3. Create Your First WiFi Network
- Click "Networks" → "Create Network"
- Fill in:
  - Source Device (your registered device)
  - Network Name (SSID)
  - Security Type (WPA2 recommended)
  - Frequency Band (2.4GHz or 5GHz)
  - Channel number
  - Max Devices
  - Password (if security type is not "Open")
- Click "Create Network"

### 4. Share Network with Friends
- Go to your network details
- Click "Share"
- Select a user to share with
- Choose permission level:
  - **View Only**: Can see network details
  - **Can Connect**: Can connect to the network
  - **Can Manage**: Can modify network settings
- Click "Share Network"

### 5. Send Network Invitations
- Click "Send Invitation" on network details
- Select user to invite
- Set expiration date (default: 7 days)
- Click "Send Invitation"

Invited users will see pending invitations on their dashboard and can accept or reject them.

## Admin Panel Guide

### User Management
- **Admin Panel** → Users
- Create/edit user accounts
- Manage permissions
- View user activity

### Device Management
- **Admin Panel** → Devices
- View all devices
- Filter by type or status
- Search by MAC address or device name
- See device details and connections

### Network Management
- **Admin Panel** → WiFi Networks
- View all networks
- Check active connections
- Modify network settings
- View security configurations

### Share Management
- **Admin Panel** → Network Shares
- View all shares
- Manage permissions
- Check expiration status
- Revoke shares

### Invitation Management
- **Admin Panel** → Network Invitations
- View all invitations
- Check invitation status
- See acceptance/rejection history

## Database Reset (Development Only)

If you need to reset the database and start fresh:

```bash
# Delete the database file
del db.sqlite3

# Recreate migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create new superuser
python manage.py createsuperuser
```

## Common Issues & Solutions

### Issue: "No such table" Error
**Solution**: Run migrations
```bash
python manage.py migrate
```

### Issue: Migration Conflicts
**Solution**: Check migration status and fix conflicts
```bash
python manage.py showmigrations
python manage.py migrate --fake filesharing 0001
python manage.py migrate
```

### Issue: Port 8000 Already in Use
**Solution**: Use a different port
```bash
python manage.py runserver 8001
```

### Issue: Static Files Not Loading
**Solution**: Collect static files
```bash
python manage.py collectstatic --noinput
```

### Issue: Can't Login to Admin
**Solution**: Create a new superuser
```bash
python manage.py createsuperuser
```

## Database Models Overview

### Device
Represents a device that can share or connect to WiFi networks.
- Device name, type, MAC address
- Online/offline status
- Last seen timestamp

### WiFiNetwork
Represents a WiFi network that can be shared.
- SSID, password, security type
- Frequency band, channel, signal strength
- Connected device tracking
- Owner and source device

### SharedNetwork
Tracks devices connected to a shared network.
- Connection quality
- Data usage
- Connection timestamps

### NetworkShare
Manages network sharing permissions.
- Permission levels (View, Connect, Manage)
- Expiration dates
- Active/inactive status

### NetworkInvitation
Handles network invitation workflow.
- Invitation status (Pending, Accepted, Rejected, Expired)
- Expiration dates
- Response tracking

## Performance Tips

1. **Use Pagination**: For large datasets, implement pagination
2. **Cache Database Queries**: Use Django's caching framework
3. **Index Important Fields**: Add database indexes for frequently searched fields
4. **Use Select Related**: Optimize database queries with select_related()
5. **Monitor Performance**: Use Django Debug Toolbar in development

## Security Checklist

- [ ] Change DEBUG to False in production
- [ ] Generate new SECRET_KEY
- [ ] Configure ALLOWED_HOSTS
- [ ] Use environment variables for sensitive data
- [ ] Enable HTTPS
- [ ] Configure CSRF protection
- [ ] Use strong passwords
- [ ] Regular security updates
- [ ] Set up proper logging
- [ ] Configure firewall rules

## Next Steps

1. Customize the application branding
2. Add email notifications
3. Implement real-time updates with WebSockets
4. Set up automated backups
5. Configure production server (Gunicorn, Nginx)
6. Add comprehensive test coverage
7. Implement analytics dashboard
8. Add mobile app integration

## Support & Documentation

- Official Django Documentation: https://docs.djangoproject.com/
- Bootstrap Documentation: https://getbootstrap.com/docs/5.3/
- Font Awesome Icons: https://fontawesome.com/icons

## Additional Resources

- Database Model Relationships: See `filesharing/models.py`
- URL Configuration: See `filesharing/urls.py`
- Form Definitions: See `filesharing/forms.py`
- View Logic: See `filesharing/views.py`
- Admin Configuration: See `filesharing/admin.py`

---

**Happy Sharing! 🎉**
