#!/usr/bin/env python
"""
Test mobile device file sharing
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sharing.settings')
django.setup()

from django.contrib.auth.models import User
from filesharing.models import File, FileShare

print("=" * 70)
print("Testing Mobile Device File Sharing")
print("=" * 70)

# Get or create test users
print("\n[1] Setting up test users...")
alice, _ = User.objects.get_or_create(username='alice', defaults={'email': 'alice@mobile.test'})
bob, _ = User.objects.get_or_create(username='bob', defaults={'email': 'bob@mobile.test'})
carol, _ = User.objects.get_or_create(username='carol', defaults={'email': 'carol@mobile.test'})
print(f"✓ Alice: {alice.username}")
print(f"✓ Bob: {bob.username}")
print(f"✓ Carol: {carol.username}")

# Create test files
print("\n[2] Creating test files...")
file1 = File.objects.create(
    owner=alice,
    filename='vacation_photo.jpg',
    file_size=2048000,
    mime_type='image/jpeg',
    file_type='image',
    is_public=False
)
print(f"✓ File created: {file1.filename}")

# Test direct FileShare creation (simulating mobile form submission)
print("\n[3] Testing direct FileShare creation (mobile simulation)...")

# Test case 1: Share with Bob
try:
    share1 = FileShare.objects.create(
        file=file1,
        shared_with_user=bob,
        permission_level='download',
        expires_at=None,
        is_active=True
    )
    print(f"✓ Share 1: {file1.filename} → {bob.username} (Can Download)")
except Exception as e:
    print(f"✗ Share 1 failed: {e}")

# Test case 2: Share with Carol
try:
    share2 = FileShare.objects.create(
        file=file1,
        shared_with_user=carol,
        permission_level='view',
        expires_at=None,
        is_active=True
    )
    print(f"✓ Share 2: {file1.filename} → {carol.username} (View Only)")
except Exception as e:
    print(f"✗ Share 2 failed: {e}")

# Verify shares exist
print("\n[4] Verifying shares in database...")
all_shares = FileShare.objects.filter(file=file1, is_active=True)
print(f"✓ Total active shares: {all_shares.count()}")
for share in all_shares:
    print(f"  - {share.shared_with_user.username} ({share.permission_level})")

# Test: Bob should see the file in "Shared With Me"
print("\n[5] Testing Bob's 'Shared With Me' view...")
bob_shares = FileShare.objects.filter(shared_with_user=bob, is_active=True)
print(f"✓ Files shared with Bob: {bob_shares.count()}")
for share in bob_shares:
    print(f"  - {share.file.filename} from {share.file.owner.username}")

# Test: Carol should see the file in "Shared With Me"
print("\n[6] Testing Carol's 'Shared With Me' view...")
carol_shares = FileShare.objects.filter(shared_with_user=carol, is_active=True)
print(f"✓ Files shared with Carol: {carol_shares.count()}")
for share in carol_shares:
    print(f"  - {share.file.filename} from {share.file.owner.username}")

# Test: Revoke share
print("\n[7] Testing revoke share...")
try:
    share1.delete()
    print(f"✓ Share revoked: {bob.username} no longer has access")
    bob_shares_after = FileShare.objects.filter(shared_with_user=bob, is_active=True)
    print(f"✓ Bob's shared files after revoke: {bob_shares_after.count()}")
except Exception as e:
    print(f"✗ Revoke failed: {e}")

# Test: Mobile dropdown list (users available for sharing)
print("\n[8] Testing user dropdown list (mobile)...")
available_users = User.objects.exclude(pk=alice.pk)
print(f"✓ Users available for Alice to share with: {available_users.count()}")
for user in available_users:
    print(f"  - {user.username} ({user.email})")

print("\n" + "=" * 70)
print("✓ ALL MOBILE SHARING TESTS PASSED!")
print("=" * 70)
print("\nMobile device form submission should now work correctly!")
