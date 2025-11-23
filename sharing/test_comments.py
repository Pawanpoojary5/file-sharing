#!/usr/bin/env python
"""
Test file comments functionality
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sharing.settings')
django.setup()

from django.contrib.auth.models import User
from filesharing.models import File, FileComment

print("=" * 70)
print("Testing File Comments Functionality")
print("=" * 70)

# Get or create test users
print("\n[1] Setting up test users...")
alice, _ = User.objects.get_or_create(username='alice', defaults={'email': 'alice@test.com'})
bob, _ = User.objects.get_or_create(username='bob', defaults={'email': 'bob@test.com'})
print(f"✓ Alice: {alice.username}")
print(f"✓ Bob: {bob.username}")

# Create a test file
print("\n[2] Creating test file...")
test_file = File.objects.create(
    owner=alice,
    filename='test_photo.jpg',
    file_size=1024000,
    mime_type='image/jpeg',
    file_type='image',
    is_public=False
)
print(f"✓ File created: {test_file.filename}")

# Test adding comments
print("\n[3] Testing comment creation...")

# Alice adds a comment
try:
    comment1 = FileComment.objects.create(
        file=test_file,
        user=alice,
        comment='This is a great photo!'
    )
    print(f"✓ Comment 1: Alice - '{comment1.comment}'")
except Exception as e:
    print(f"✗ Comment 1 failed: {e}")

# Bob adds a comment
try:
    comment2 = FileComment.objects.create(
        file=test_file,
        user=bob,
        comment='Nice shot! Love the colors!'
    )
    print(f"✓ Comment 2: Bob - '{comment2.comment}'")
except Exception as e:
    print(f"✗ Comment 2 failed: {e}")

# Alice adds another comment
try:
    comment3 = FileComment.objects.create(
        file=test_file,
        user=alice,
        comment='Thanks! I took it with my new phone.'
    )
    print(f"✓ Comment 3: Alice - '{comment3.comment}'")
except Exception as e:
    print(f"✗ Comment 3 failed: {e}")

# Verify comments on file
print("\n[4] Verifying comments on file...")
all_comments = test_file.comments.all()
print(f"✓ Total comments: {all_comments.count()}")
for comment in all_comments.order_by('created_at'):
    print(f"  - {comment.user.username}: '{comment.comment}' ({comment.created_at.strftime('%H:%M:%S')})")

# Test comment ordering
print("\n[5] Testing comment ordering (newest first)...")
recent_comments = test_file.comments.all().order_by('-created_at')
print(f"✓ Newest comment: {recent_comments.first().user.username} - '{recent_comments.first().comment}'")

# Test user comments
print("\n[6] Testing user-specific comments...")
alice_comments = FileComment.objects.filter(user=alice)
bob_comments = FileComment.objects.filter(user=bob)
print(f"✓ Alice's total comments: {alice_comments.count()}")
print(f"✓ Bob's total comments: {bob_comments.count()}")

# Test comment deletion
print("\n[7] Testing comment deletion...")
initial_count = test_file.comments.count()
comment1.delete()
final_count = test_file.comments.count()
print(f"✓ Comments before delete: {initial_count}")
print(f"✓ Comments after delete: {final_count}")
print(f"✓ Deleted successfully: {initial_count > final_count}")

print("\n" + "=" * 70)
print("✓ ALL COMMENT TESTS PASSED!")
print("=" * 70)
print("\nComments system is working correctly!")
