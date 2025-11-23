# 📱💻 Connect Smartphone to Laptop - File Sharing Guide

## **What You Need**
1. ✅ Smartphone (Android/iOS)
2. ✅ Laptop (Windows/Mac/Linux)
3. ✅ Same WiFi Network (both devices on same WiFi)
4. ✅ Django app running on laptop

---

## **STEP 1: Start Django Server on Laptop**

Open PowerShell/Terminal on your laptop:

```bash
cd c:\file_sharing\sharing
python manage.py runserver 0.0.0.0:8000
```

You'll see:
```
Starting development server at http://0.0.0.0:8000/
```

**Find Your Laptop IP Address:**

In PowerShell, run:
```bash
ipconfig
```

Look for **IPv4 Address** under your WiFi adapter (usually looks like `192.168.x.x` or `10.x.x.x`)

Example: `192.168.1.100`

---

## **STEP 2: Connect Smartphone to Same WiFi**

On your **smartphone**:
1. Go to **Settings** → **WiFi**
2. Find your WiFi network name
3. Connect to it (enter password if needed)

✅ Both devices now on same network!

---

## **STEP 3: Access App from Smartphone Browser**

On your **smartphone**, open any browser (Chrome, Safari, Firefox):

**Type in address bar:**
```
http://192.168.1.100:8000
```

Replace `192.168.1.100` with your **actual laptop IP address**

Press **Enter** → App loads on smartphone! 🎉

---

## **STEP 4: Create Account (First Time Only)**

On smartphone browser:
1. Click **"Sign Up"** button
2. Create username, email, password
3. Click **"Sign Up"**

Now **logged in** on smartphone!

---

## **STEP 5: Register Device on Smartphone**

On smartphone browser:
1. Click **"Devices"** menu → **"Register Device"**
2. Device Name: `My Phone` (or any name)
3. Device Type: **Mobile**
4. MAC Address: Find it in phone settings
   - **Android**: Settings → About Phone → Status
   - **iOS**: Settings → General → About → WiFi Address
5. Click **"Register Device"** ✅

---

## **STEP 6: Upload File on Laptop**

On **laptop browser** (at http://localhost:8000):
1. **Login** with your account
2. Click **"Files"** menu (top navigation)
3. Click **"Upload File"**
4. Select a file from your computer
5. Click **"Upload File"** ✅

File now uploaded to your account!

---

## **STEP 7: Share File with Smartphone**

On **laptop browser**:
1. Click **"Files"** → **"My Files"**
2. Click on the file you uploaded
3. Scroll down to **"Share This File"** section
4. Select your phone username from dropdown
5. Choose permission: **"Can Download"** (or "View Only")
6. Click **"Share"** ✅

---

## **STEP 8: Download File on Smartphone**

On **smartphone browser**:
1. Click **"Files"** menu
2. Click **"Shared With Me"**
3. You should see the file shared from laptop
4. Click on the file
5. Click **"Download"** button ✅

**File downloaded to smartphone!** 📥

---

## **STEP 9: Upload File from Smartphone, Download on Laptop**

**Reverse direction:**

On **smartphone browser**:
1. Click **"Files"** → **"Upload File"**
2. Select a photo or file from phone
3. Click **"Upload File"** ✅

On **laptop browser**:
1. Click **"Files"** → **"My Files"**
2. Click the file
3. Click **"Download"** button
4. File saved to laptop! 💾

---

## **Quick Navigation Menu**

```
📱 On Smartphone Browser:
   ├── Files
   │   ├── My Files (upload here)
   │   ├── Upload File (new files)
   │   └── Shared With Me (receive files)
   ├── Devices
   │   ├── My Devices
   │   └── Register Device
   ├── Networks
   │   ├── My Networks
   │   ├── Create Network
   │   └── Shared With Me
   └── Profile
```

---

## **Common IP Addresses**

| WiFi Type | Common IP Range |
|-----------|-----------------|
| Home WiFi | 192.168.0.x, 192.168.1.x |
| Mobile Hotspot | 192.168.43.x, 10.0.0.x |
| Office WiFi | Varies (ask admin) |

**To check your IP:**
- **Windows**: `ipconfig` in PowerShell
- **Mac/Linux**: `ifconfig` in Terminal

---

## **Troubleshooting**

### ❌ "Can't connect to 192.168.x.x:8000"

**Solution 1:** Check both devices on same WiFi
```bash
# On laptop, verify server is running
python manage.py runserver 0.0.0.0:8000
```

**Solution 2:** Check Windows Firewall allows port 8000
- Press `Win + R` → type `wf.msc`
- Click "Inbound Rules" → "New Rule"
- Allow port 8000

**Solution 3:** Verify correct IP address
```bash
ipconfig  # Run on laptop to get correct IP
```

### ❌ "Smartphone can't see laptop"

**Check:**
1. Both on same WiFi network
2. No WiFi Guest Network (use main WiFi)
3. Firewall not blocking
4. Django server running (`python manage.py runserver 0.0.0.0:8000`)

### ❌ "File won't download"

**Check:**
1. File uploaded successfully (shows in "My Files")
2. Shared with correct user
3. Permission level set to "Can Download"
4. User logged in on smartphone

---

## **Tips & Tricks**

✅ **Public Files** - Upload file → Check "Make Public" → Share link with anyone on network

✅ **Quick Upload** - Use drag-and-drop on "Upload File" page (works on both laptop & smartphone)

✅ **Set Expiry Date** - When sharing, set expiry date (file access auto-revoked)

✅ **View Before Download** - Click file first to preview before downloading

✅ **Comments** - Add comments to files for notes/feedback

✅ **Download Tracking** - See how many times a file was downloaded

---

## **Example Workflow**

### **Scenario: Send Photos from Phone to Laptop**

```
1. Open phone browser → http://192.168.1.100:8000
2. Login with account
3. Click "Files" → "Upload File"
4. Select 3 photos from phone gallery
5. Upload each photo
6. Open laptop browser → login
7. Click "Files" → "My Files"
8. See all 3 photos uploaded ✅
9. Download to laptop
```

### **Scenario: Send Work Document from Laptop to Phone**

```
1. On laptop: Click "Files" → "Upload File"
2. Upload PDF or Word document
3. Click on file → "Share"
4. Share with your phone user account
5. On phone browser: Click "Files" → "Shared With Me"
6. Download file to phone ✅
```

---

## **Production Setup (Optional)**

When ready to use outside your home network:

1. **Get Domain Name** (example.com)
2. **Setup Firewall** - Port forward 8000 to laptop
3. **Use HTTPS** - Install SSL certificate
4. **Deploy** - Use PythonAnywhere or Heroku

For now, this local network setup is perfect for testing! 🚀

---

## **Questions?**

If something doesn't work:
1. Check server is running: `python manage.py runserver 0.0.0.0:8000`
2. Check correct IP: `ipconfig` on laptop
3. Check both on same WiFi
4. Restart browser on smartphone
5. Clear browser cache if issues persist

**Happy file sharing!** 📱💻✅
