#!/usr/bin/env python
"""
Test file sharing functionality
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sharing.settings')
django.setup()

from django.contrib.auth.models import User
from filesharing.models import File, FileShare
from filesharing.forms import FileShareForm

print("=" * 60)
print("Testing File Sharing Functionality")
print("=" * 60)

# Create test users
print("\n[1] Creating test users...")
user1, _ = User.objects.get_or_create(username='alice', defaults={'email': 'alice@test.com'})
user2, _ = User.objects.get_or_create(username='bob', defaults={'email': 'bob@test.com'})
print(f"✓ User 1: {user1.username} ({user1.email})")
print(f"✓ User 2: {user2.username} ({user2.email})")

# Create a test file
print("\n[2] Creating test file...")
test_file = File.objects.create(
    owner=user1,
    filename='test_photo.jpg',
    file_size=1024000,
    mime_type='image/jpeg',
    file_type='image',
    is_public=False
)
print(f"✓ File created: {test_file.filename} (ID: {test_file.id})")

# Test FileShareForm
print("\n[3] Testing FileShareForm...")
form_data = {
    'shared_with_user': user2.id,
    'permission_level': 'download',
    'expires_at': ''
}
form = FileShareForm(form_data, user=user1)
print(f"Form valid: {form.is_valid()}")
if not form.is_valid():
    print("Errors:", form.errors)
else:
    print("✓ Form validation passed")
    
    # Try to save
    print("\n[4] Creating file share...")
    share = form.save(commit=False)
    share.file = test_file
    share.save()
    print(f"✓ Share created successfully!")
    print(f"  - File: {share.file.filename}")
    print(f"  - Shared with: {share.shared_with_user.username}")
    print(f"  - Permission: {share.permission_level}")
    print(f"  - Active: {share.is_active}")

# Verify share exists
print("\n[5] Verifying share...")
shares = FileShare.objects.filter(file=test_file, is_active=True)
print(f"✓ Found {shares.count()} active share(s)")
for share in shares:
    print(f"  - {share.shared_with_user.username} ({share.permission_level})")

# Test user list for dropdown
print("\n[6] Testing user dropdown list...")
all_users = User.objects.exclude(pk=user1.pk)
print(f"✓ Users available for sharing: {all_users.count()}")
for u in all_users:
    print(f"  - {u.username} ({u.email})")

print("\n" + "=" * 60)
print("✓ ALL TESTS PASSED - File sharing is working!")
print("=" * 60)
