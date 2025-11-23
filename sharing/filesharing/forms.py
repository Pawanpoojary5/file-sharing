from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Device, WiFiNetwork, SharedNetwork, NetworkShare, NetworkInvitation, File, FileShare, FileComment
import re


class DeviceRegistrationForm(forms.ModelForm):
    """Form for registering a new device"""
    mac_address = forms.CharField(
        max_length=17,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'XX:XX:XX:XX:XX:XX',
            'pattern': '[A-Fa-f0-9]{2}(?::[A-Fa-f0-9]{2}){5}'
        }),
        help_text='Enter MAC address in format XX:XX:XX:XX:XX:XX'
    )
    
    class Meta:
        model = Device
        fields = ['device_name', 'device_type', 'mac_address', 'ip_address']
        widgets = {
            'device_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., My Laptop'
            }),
            'device_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'ip_address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '192.168.1.100 (optional)',
                'required': False
            })
        }
    
    def clean_mac_address(self):
        mac = self.cleaned_data.get('mac_address').upper()
        if not re.match(r'^([0-9A-F]{2}:){5}([0-9A-F]{2})$', mac):
            raise forms.ValidationError('Invalid MAC address format')
        return mac


class WiFiNetworkForm(forms.ModelForm):
    """Form for creating and updating WiFi networks"""
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Network password'
        }),
        help_text='Leave empty for open networks'
    )
    
    class Meta:
        model = WiFiNetwork
        fields = ['source_device', 'network_name', 'password', 'security_type', 
                  'frequency_band', 'channel', 'signal_strength', 'max_devices']
        widgets = {
            'source_device': forms.Select(attrs={'class': 'form-select'}),
            'network_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Network SSID (max 32 characters)',
                'maxlength': '32'
            }),
            'security_type': forms.Select(attrs={'class': 'form-select'}),
            'frequency_band': forms.Select(attrs={'class': 'form-select'}),
            'channel': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '165'
            }),
            'signal_strength': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '-100',
                'max': '-30'
            }),
            'max_devices': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            })
        }
    
    def clean(self):
        cleaned_data = super().clean()
        security_type = cleaned_data.get('security_type')
        password = cleaned_data.get('password')
        
        if security_type != 'open' and not password:
            raise forms.ValidationError('Password required for secured networks')
        
        if password and len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters')
        
        return cleaned_data


class ShareNetworkForm(forms.ModelForm):
    """Form for sharing networks with other users"""
    shared_with_user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-select',
            'placeholder': 'Select user'
        }),
        label='Share with user'
    )
    
    class Meta:
        model = NetworkShare
        fields = ['permission_level', 'expires_at']
        widgets = {
            'permission_level': forms.RadioSelect(choices=[
                ('view', 'View Only'),
                ('connect', 'Can Connect'),
                ('manage', 'Can Manage'),
            ]),
            'expires_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'required': False
            })
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['shared_with_user'].queryset = User.objects.exclude(pk=user.pk)


class NetworkInvitationForm(forms.ModelForm):
    """Form for sending network invitations"""
    invited_user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Invite user'
    )
    
    class Meta:
        model = NetworkInvitation
        fields = ['invited_user', 'expires_at']
        widgets = {
            'expires_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            })
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['invited_user'].queryset = User.objects.exclude(pk=user.pk)


class UserRegistrationForm(UserCreationForm):
    """Form for user registration"""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email address'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })


class UserProfileForm(UserChangeForm):
    """Form for updating user profile"""
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UpdateDeviceForm(forms.ModelForm):
    """Form for updating device information"""
    class Meta:
        model = Device
        fields = ['device_name', 'device_type', 'ip_address']
        widgets = {
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'device_type': forms.Select(attrs={'class': 'form-select'}),
            'ip_address': forms.TextInput(attrs={'class': 'form-control'})
        }


class UpdateNetworkForm(forms.ModelForm):
    """Form for updating network settings"""
    class Meta:
        model = WiFiNetwork
        fields = ['network_name', 'password', 'channel', 'signal_strength', 'max_devices', 'is_active']
        widgets = {
            'network_name': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'channel': forms.NumberInput(attrs={'class': 'form-control'}),
            'signal_strength': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_devices': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


# ============ FILE SHARING FORMS ============

class FileUploadForm(forms.ModelForm):
    """Form for uploading files"""
    class Meta:
        model = File
        fields = ['file', 'is_public']
        widgets = {
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '*/*'
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_public'].label = 'Make file public (anyone with link can view)'


class FileShareForm(forms.ModelForm):
    """Form for sharing files with other users"""
    shared_with_user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-select',
            'placeholder': 'Select user'
        }),
        label='Share with user'
    )
    
    class Meta:
        model = FileShare
        fields = ['shared_with_user', 'permission_level', 'expires_at']
        widgets = {
            'permission_level': forms.RadioSelect(choices=[
                ('view', 'View Only'),
                ('download', 'Can Download'),
            ]),
            'expires_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'required': False
            })
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['shared_with_user'].queryset = User.objects.exclude(pk=user.pk)


class FileCommentForm(forms.ModelForm):
    """Form for commenting on files"""
    class Meta:
        model = FileComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Add a comment...',
                'rows': 3
            })
        }
