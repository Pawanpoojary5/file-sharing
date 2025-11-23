from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class Device(models.Model):
    """Represents a device that can share or connect to WiFi networks"""
    DEVICE_TYPE_CHOICES = [
        ('laptop', 'Laptop'),
        ('phone', 'Smartphone'),
        ('tablet', 'Tablet'),
        ('router', 'Router'),
        ('hotspot', 'Hotspot Device'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    device_name = models.CharField(max_length=100)
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPE_CHOICES)
    mac_address = models.CharField(max_length=17, unique=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    is_online = models.BooleanField(default=True)
    last_seen = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-last_seen']
    
    def __str__(self):
        return f"{self.device_name} ({self.device_type})"


class WiFiNetwork(models.Model):
    """Represents a WiFi network that can be shared"""
    SECURITY_CHOICES = [
        ('open', 'Open Network'),
        ('wep', 'WEP'),
        ('wpa', 'WPA'),
        ('wpa2', 'WPA2'),
        ('wpa3', 'WPA3'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wifi_networks')
    source_device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='shared_networks')
    network_name = models.CharField(max_length=32)  # SSID
    password = models.CharField(max_length=63, blank=True)
    security_type = models.CharField(max_length=10, choices=SECURITY_CHOICES, default='wpa2')
    frequency_band = models.CharField(max_length=10, choices=[('2.4GHz', '2.4GHz'), ('5GHz', '5GHz'), ('6GHz', '6GHz')])
    channel = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(165)])
    signal_strength = models.IntegerField(validators=[MinValueValidator(-100), MaxValueValidator(-30)], default=-50)
    max_devices = models.IntegerField(default=32, validators=[MinValueValidator(1)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('owner', 'network_name')
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.network_name} - {self.security_type}"
    
    def connected_devices_count(self):
        return self.connected_devices.filter(is_connected=True).count()


class SharedNetwork(models.Model):
    """Tracks devices connected to a shared WiFi network"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    network = models.ForeignKey(WiFiNetwork, on_delete=models.CASCADE, related_name='connected_devices')
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='connected_networks')
    is_connected = models.BooleanField(default=True)
    connection_quality = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=100)
    data_used = models.BigIntegerField(default=0)  # in bytes
    connected_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('network', 'device')
        ordering = ['-last_activity']
    
    def __str__(self):
        return f"{self.device.device_name} -> {self.network.network_name}"


class NetworkShare(models.Model):
    """Manages sharing permissions for networks"""
    PERMISSION_CHOICES = [
        ('view', 'View Only'),
        ('connect', 'Can Connect'),
        ('manage', 'Can Manage'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    network = models.ForeignKey(WiFiNetwork, on_delete=models.CASCADE, related_name='shares')
    shared_with_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_networks_with_me')
    permission_level = models.CharField(max_length=10, choices=PERMISSION_CHOICES, default='connect')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('network', 'shared_with_user')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.network.network_name} shared with {self.shared_with_user.username}"


class NetworkInvitation(models.Model):
    """Invitations to join shared networks"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    network = models.ForeignKey(WiFiNetwork, on_delete=models.CASCADE, related_name='invitations')
    invited_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='network_invitations')
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    responded_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('network', 'invited_user')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Invitation: {self.network.network_name} to {self.invited_user.username}"


# ============ FILE SHARING MODELS ============

class File(models.Model):
    """Represents an uploaded file"""
    FILE_TYPE_CHOICES = [
        ('image', 'Image'),
        ('document', 'Document'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('archive', 'Archive'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')
    file = models.FileField(upload_to='files/%Y/%m/%d/')
    filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=20, choices=FILE_TYPE_CHOICES, default='other')
    file_size = models.BigIntegerField()  # in bytes
    mime_type = models.CharField(max_length=100, blank=True)
    is_public = models.BooleanField(default=False)
    download_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['owner', '-created_at']),
            models.Index(fields=['is_public']),
        ]
    
    def __str__(self):
        return f"{self.filename} ({self.owner.username})"
    
    def get_file_icon(self):
        """Return Font Awesome icon class based on file type"""
        icons = {
            'image': 'fa-image',
            'document': 'fa-file-pdf',
            'video': 'fa-video',
            'audio': 'fa-music',
            'archive': 'fa-file-zipper',
        }
        return icons.get(self.file_type, 'fa-file')
    
    def get_display_size(self):
        """Convert bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if self.file_size < 1024:
                return f"{self.file_size:.1f} {unit}"
            self.file_size /= 1024
        return f"{self.file_size:.1f} TB"


class FileShare(models.Model):
    """Manages file sharing permissions"""
    PERMISSION_CHOICES = [
        ('view', 'View Only'),
        ('download', 'Can Download'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name='shares')
    shared_with_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_files')
    permission_level = models.CharField(max_length=10, choices=PERMISSION_CHOICES, default='download')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('file', 'shared_with_user')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.file.filename} shared with {self.shared_with_user.username}"
    
    def is_expired(self):
        """Check if share has expired"""
        if self.expires_at and timezone.now() > self.expires_at:
            return True
        return False


class FileComment(models.Model):
    """Comments on shared files"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.file.filename}"
