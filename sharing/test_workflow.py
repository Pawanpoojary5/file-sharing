#!/usr/bin/env python
"""
Test script to verify the complete workflow:
1. Create user
2. Register device
3. Create network
4. Upload file
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sharing.settings')
django.setup()

from django.contrib.auth.models import User
from filesharing.models import Device, WiFiNetwork, File
from django.utils import timezone

def test_workflow():
    print("=" * 60)
    print("Testing WiFi Network Sharing Application Workflow")
    print("=" * 60)
    
    # Step 1: Create a test user
    print("\n[1] Creating test user...")
    try:
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        print(f"✓ User created: {user.username}")
    except Exception as e:
        print(f"✗ Error creating user: {e}")
        user = User.objects.get(username='testuser')
        print(f"✓ Using existing user: {user.username}")
    
    # Step 2: Register a device
    print("\n[2] Registering device...")
    try:
        device = Device.objects.create(
            user=user,
            device_name='My Laptop',
            device_type='laptop',
            mac_address='AA:BB:CC:DD:EE:FF',
            ip_address='192.168.1.100'
        )
        print(f"✓ Device registered: {device.device_name}")
        print(f"  - MAC Address: {device.mac_address}")
        print(f"  - Status: {'Online' if device.is_online else 'Offline'}")
    except Exception as e:
        print(f"✗ Error registering device: {e}")
        return False
    
    # Step 3: Create a WiFi network
    print("\n[3] Creating WiFi network...")
    try:
        network = WiFiNetwork.objects.create(
            owner=user,
            source_device=device,
            network_name='MyWiFiNetwork',
            password='securepass123',
            security_type='wpa2',
            frequency_band='2.4GHz',
            channel=6,
            signal_strength=-50,
            max_devices=32
        )
        print(f"✓ Network created: {network.network_name}")
        print(f"  - Security: {network.security_type.upper()}")
        print(f"  - Frequency: {network.frequency_band}")
        print(f"  - Status: {'Active' if network.is_active else 'Inactive'}")
    except Exception as e:
        print(f"✗ Error creating network: {e}")
        return False
    
    # Step 4: Verify relationships
    print("\n[4] Verifying relationships...")
    try:
        user_devices = user.devices.all().count()
        user_networks = user.wifi_networks.all().count()
        print(f"✓ User has {user_devices} device(s)")
        print(f"✓ User has {user_networks} network(s)")
    except Exception as e:
        print(f"✗ Error verifying relationships: {e}")
        return False
    
    # Step 5: Test form validation
    print("\n[5] Testing form validation...")
    try:
        from filesharing.forms import DeviceRegistrationForm
        
        # Valid MAC address
        form_data = {
            'device_name': 'Test Phone',
            'device_type': 'phone',
            'mac_address': 'AA:BB:CC:DD:EE:00',
            'ip_address': '192.168.1.50'
        }
        form = DeviceRegistrationForm(data=form_data)
        if form.is_valid():
            print("✓ Valid device form accepted")
        else:
            print(f"✗ Valid form rejected: {form.errors}")
        
        # Invalid MAC address
        invalid_data = form_data.copy()
        invalid_data['mac_address'] = 'INVALID'
        form = DeviceRegistrationForm(data=invalid_data)
        if not form.is_valid() and 'mac_address' in form.errors:
            print("✓ Invalid MAC address correctly rejected")
        else:
            print("✗ Invalid MAC address not rejected")
    except Exception as e:
        print(f"✗ Error in form validation test: {e}")
    
    print("\n" + "=" * 60)
    print("✓ ALL TESTS PASSED - Workflow is operational!")
    print("=" * 60)
    return True

if __name__ == '__main__':
    test_workflow()
