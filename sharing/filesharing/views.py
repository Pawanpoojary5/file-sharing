from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q, Count, Sum
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta, datetime
import json

from .forms import (
    DeviceRegistrationForm, WiFiNetworkForm, ShareNetworkForm,
    NetworkInvitationForm, UserRegistrationForm, UserProfileForm,
    UpdateDeviceForm, UpdateNetworkForm, FileUploadForm, FileShareForm, FileCommentForm
)
from .models import Device, WiFiNetwork, SharedNetwork, NetworkShare, NetworkInvitation, File, FileShare, FileComment


# ============ Authentication Views ============

def home(request):
    """Landing page"""
    if request.user.is_authenticated:
        return redirect('filesharing:dashboard')
    
    context = {
        'title': 'WiFi Network Sharing Platform',
        'message': 'Share WiFi networks securely with your devices and friends'
    }
    return render(request, 'home.html', context)


def signup_view(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect('filesharing:dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('filesharing:dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegistrationForm()
    
    return render(request, 'auth/signup.html', {'form': form})


def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('filesharing:dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('filesharing:dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    else:
        form = AuthenticationForm()
    
    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('filesharing:home')


# ============ Dashboard Views ============

@login_required
def dashboard(request):
    """Main dashboard"""
    user = request.user
    
    # Get user stats
    devices = user.devices.all()
    networks = user.wifi_networks.all()
    shared_networks = user.shared_networks_with_me.filter(is_active=True)
    pending_invitations = user.network_invitations.filter(status='pending')
    
    # Active connections
    active_connections = SharedNetwork.objects.filter(
        network__owner=user,
        is_connected=True
    ).count()
    
    context = {
        'devices_count': devices.count(),
        'networks_count': networks.count(),
        'shared_networks_count': shared_networks.count(),
        'active_connections': active_connections,
        'pending_invitations': pending_invitations.count(),
        'recent_networks': networks[:5],
        'recent_devices': devices[:5],
        'pending_invitations_list': pending_invitations[:5],
    }
    
    return render(request, 'dashboard/index.html', context)


# ============ Device Management Views ============

@login_required
def devices_list(request):
    """List all devices for the user"""
    devices = request.user.devices.all()
    
    context = {
        'devices': devices,
        'page_title': 'My Devices',
    }
    
    return render(request, 'devices/list.html', context)


@login_required
def register_device(request):
    """Register a new device"""
    if request.method == 'POST':
        form = DeviceRegistrationForm(request.POST)
        if form.is_valid():
            device = form.save(commit=False)
            device.user = request.user
            device.save()
            messages.success(request, f'Device "{device.device_name}" registered successfully!')
            return redirect('filesharing:devices-list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = DeviceRegistrationForm()
    
    context = {
        'form': form,
        'page_title': 'Register New Device',
    }
    
    return render(request, 'devices/register.html', context)


@login_required
def device_detail(request, pk):
    """View device details"""
    device = get_object_or_404(Device, pk=pk, user=request.user)
    
    # Get networks this device is connected to
    connections = device.connected_networks.all()
    
    context = {
        'device': device,
        'connections': connections,
        'page_title': f'Device - {device.device_name}',
    }
    
    return render(request, 'devices/detail.html', context)


@login_required
def edit_device(request, pk):
    """Edit device information"""
    device = get_object_or_404(Device, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = UpdateDeviceForm(request.POST, instance=device)
        if form.is_valid():
            form.save()
            messages.success(request, 'Device updated successfully!')
            return redirect('filesharing:device-edit', pk=device.pk)
    else:
        form = UpdateDeviceForm(instance=device)
    
    context = {
        'form': form,
        'device': device,
        'page_title': f'Edit - {device.device_name}',
    }
    
    return render(request, 'devices/edit.html', context)


@login_required
@require_http_methods(["POST"])
def delete_device(request, pk):
    """Delete a device"""
    device = get_object_or_404(Device, pk=pk, user=request.user)
    device_name = device.device_name
    device.delete()
    messages.success(request, f'Device "{device_name}" deleted successfully!')
    return redirect('filesharing:devices-list')


# ============ WiFi Network Views ============

@login_required
def networks_list(request):
    """List all WiFi networks owned by user"""
    networks = request.user.wifi_networks.all()
    
    context = {
        'networks': networks,
        'page_title': 'My WiFi Networks',
    }
    
    return render(request, 'networks/list.html', context)


@login_required
def create_network(request):
    """Create a new WiFi network"""
    user_devices = request.user.devices.all()
    
    if not user_devices.exists():
        messages.warning(request, 'Please register a device first before creating a network.')
        return redirect('filesharing:register-device')
    
    if request.method == 'POST':
        form = WiFiNetworkForm(request.POST)
        if form.is_valid():
            network = form.save(commit=False)
            network.owner = request.user
            network.save()
            messages.success(request, f'Network "{network.network_name}" created successfully!')
            return redirect('filesharing:network-detail', pk=network.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = WiFiNetworkForm()
        form.fields['source_device'].queryset = user_devices
    
    context = {
        'form': form,
        'page_title': 'Create New WiFi Network',
    }
    
    return render(request, 'networks/create.html', context)


@login_required
def network_detail(request, pk):
    """View WiFi network details"""
    network = get_object_or_404(WiFiNetwork, pk=pk, owner=request.user)
    
    # Get connected devices
    connected_devices = network.connected_devices.filter(is_connected=True)
    
    # Get shares
    shares = network.shares.filter(is_active=True)
    
    # Get pending invitations
    invitations = network.invitations.filter(status='pending')
    
    context = {
        'network': network,
        'connected_devices': connected_devices,
        'shares': shares,
        'invitations': invitations,
        'page_title': f'Network - {network.network_name}',
    }
    
    return render(request, 'networks/detail.html', context)


@login_required
def edit_network(request, pk):
    """Edit WiFi network settings"""
    network = get_object_or_404(WiFiNetwork, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        form = UpdateNetworkForm(request.POST, instance=network)
        if form.is_valid():
            form.save()
            messages.success(request, 'Network updated successfully!')
            return redirect('filesharing:network-detail', pk=network.pk)
    else:
        form = UpdateNetworkForm(instance=network)
    
    context = {
        'form': form,
        'network': network,
        'page_title': f'Edit - {network.network_name}',
    }
    
    return render(request, 'networks/edit.html', context)


@login_required
@require_http_methods(["POST"])
def delete_network(request, pk):
    """Delete a WiFi network"""
    network = get_object_or_404(WiFiNetwork, pk=pk, owner=request.user)
    network_name = network.network_name
    network.delete()
    messages.success(request, f'Network "{network_name}" deleted successfully!')
    return redirect('filesharing:networks-list')


# ============ Network Sharing Views ============

@login_required
def share_network(request, pk):
    """Share a network with another user"""
    network = get_object_or_404(WiFiNetwork, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        form = ShareNetworkForm(request.POST, user=request.user)
        if form.is_valid():
            share = form.save(commit=False)
            share.network = network
            share.save()
            messages.success(request, f'Network shared with {share.shared_with_user.username}!')
            return redirect('filesharing:network-detail', pk=network.pk)
    else:
        form = ShareNetworkForm(user=request.user)
    
    context = {
        'form': form,
        'network': network,
        'page_title': f'Share - {network.network_name}',
    }
    
    return render(request, 'networks/share.html', context)


@login_required
@require_http_methods(["POST"])
def revoke_share(request, network_pk, share_pk):
    """Revoke network share"""
    network = get_object_or_404(WiFiNetwork, pk=network_pk, owner=request.user)
    share = get_object_or_404(NetworkShare, pk=share_pk, network=network)
    
    username = share.shared_with_user.username
    share.delete()
    messages.success(request, f'Share with {username} revoked!')
    
    return redirect('filesharing:network-detail', pk=network.pk)


# ============ Network Invitation Views ============

@login_required
def send_invitation(request, pk):
    """Send network invitation"""
    network = get_object_or_404(WiFiNetwork, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        form = NetworkInvitationForm(request.POST, user=request.user)
        if form.is_valid():
            invitation = form.save(commit=False)
            invitation.network = network
            invitation.invited_by = request.user
            invitation.save()
            messages.success(request, f'Invitation sent to {invitation.invited_user.username}!')
            return redirect('filesharing:network-detail', pk=network.pk)
    else:
        # Default expiry: 7 days from now
        default_expiry = timezone.now() + timedelta(days=7)
        form = NetworkInvitationForm(user=request.user, initial={'expires_at': default_expiry})
    
    context = {
        'form': form,
        'network': network,
        'page_title': f'Send Invitation - {network.network_name}',
    }
    
    return render(request, 'networks/invite.html', context)


@login_required
def invitations(request):
    """View pending invitations"""
    pending = request.user.network_invitations.filter(status='pending')
    
    context = {
        'pending_invitations': pending,
        'page_title': 'Network Invitations',
    }
    
    return render(request, 'invitations/list.html', context)


@login_required
@require_http_methods(["POST"])
def accept_invitation(request, pk):
    """Accept network invitation"""
    invitation = get_object_or_404(NetworkInvitation, pk=pk, invited_user=request.user)
    
    # Check if invitation hasn't expired
    if invitation.expires_at < timezone.now():
        invitation.status = 'expired'
        invitation.save()
        messages.error(request, 'Invitation has expired!')
        return redirect('filesharing:invitations')
    
    invitation.status = 'accepted'
    invitation.responded_at = timezone.now()
    invitation.save()
    
    messages.success(request, f'Invitation accepted! You can now connect to {invitation.network.network_name}')
    return redirect('filesharing:network-detail', pk=invitation.network.pk)


@login_required
@require_http_methods(["POST"])
def reject_invitation(request, pk):
    """Reject network invitation"""
    invitation = get_object_or_404(NetworkInvitation, pk=pk, invited_user=request.user)
    
    invitation.status = 'rejected'
    invitation.responded_at = timezone.now()
    invitation.save()
    
    messages.info(request, 'Invitation declined')
    return redirect('filesharing:invitations')


# ============ Shared Networks View ============

@login_required
def shared_networks(request):
    """View networks shared with the user"""
    shares = NetworkShare.objects.filter(shared_with_user=request.user, is_active=True)
    
    context = {
        'shares': shares,
        'page_title': 'Networks Shared With Me',
    }
    
    return render(request, 'networks/shared.html', context)


# ============ User Profile Views ============

@login_required
def profile(request):
    """View user profile"""
    user_devices = request.user.devices.all()
    user_networks = request.user.wifi_networks.all()
    
    context = {
        'devices_count': user_devices.count(),
        'networks_count': user_networks.count(),
        'page_title': 'My Profile',
    }
    
    return render(request, 'profile/view.html', context)


@login_required
def edit_profile(request):
    """Edit user profile"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('filesharing:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {
        'form': form,
        'page_title': 'Edit Profile',
    }
    
    return render(request, 'profile/edit.html', context)


# ============ API Views ============

@login_required
def api_network_stats(request, pk):
    """API endpoint for network statistics"""
    network = get_object_or_404(WiFiNetwork, pk=pk, owner=request.user)
    
    connected_count = network.connected_devices.filter(is_connected=True).count()
    total_data_used = network.connected_devices.aggregate(
        total=Sum('data_used')
    )['total'] or 0
    
    data = {
        'network_name': network.network_name,
        'is_active': network.is_active,
        'connected_devices': connected_count,
        'max_devices': network.max_devices,
        'total_data_used': total_data_used,
        'signal_strength': network.signal_strength,
        'channel': network.channel,
        'frequency_band': network.frequency_band,
    }
    
    return JsonResponse(data)


@login_required
def api_device_status(request, pk):
    """API endpoint for device status"""
    device = get_object_or_404(Device, pk=pk, user=request.user)
    
    data = {
        'device_name': device.device_name,
        'device_type': device.get_device_type_display(),
        'is_online': device.is_online,
        'last_seen': device.last_seen.isoformat(),
        'ip_address': device.ip_address,
        'mac_address': device.mac_address,
    }
    
    return JsonResponse(data)


# ============ Utility Views ============

@login_required
def search(request):
    """Search across networks and devices"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        networks = []
        devices = []
    else:
        networks = request.user.wifi_networks.filter(
            Q(network_name__icontains=query)
        )
        devices = request.user.devices.filter(
            Q(device_name__icontains=query)
        )
    
    context = {
        'query': query,
        'networks': networks,
        'devices': devices,
        'page_title': f'Search Results for "{query}"',
    }
    
    return render(request, 'search.html', context)


# ============ FILE SHARING VIEWS ============

def get_started(request):
    """Get started landing page with call to action"""
    if request.user.is_authenticated:
        return redirect('filesharing:files-list')
    
    context = {
        'title': 'Get Started - File Sharing',
        'message': 'Share files securely and easily'
    }
    return render(request, 'files/get_started.html', context)


@login_required
def files_list(request):
    """List all files uploaded by the current user"""
    user = request.user
    files = user.uploaded_files.all()
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(files, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get shared files count
    shared_with_me = FileShare.objects.filter(shared_with_user=user, is_active=True)
    
    context = {
        'page_obj': page_obj,
        'files': page_obj.object_list,
        'shared_count': shared_with_me.count(),
        'total_files': files.count(),
        'title': 'My Files',
    }
    return render(request, 'files/list.html', context)


@login_required
def upload_file(request):
    """Upload a new file"""
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_obj = form.save(commit=False)
            file_obj.owner = request.user
            file_obj.filename = request.FILES['file'].name
            file_obj.file_size = request.FILES['file'].size
            file_obj.mime_type = request.FILES['file'].content_type
            
            # Determine file type from mime type
            mime = file_obj.mime_type.lower()
            if mime.startswith('image'):
                file_obj.file_type = 'image'
            elif mime.startswith('video'):
                file_obj.file_type = 'video'
            elif mime.startswith('audio'):
                file_obj.file_type = 'audio'
            elif 'pdf' in mime or 'document' in mime or 'word' in mime or 'spreadsheet' in mime:
                file_obj.file_type = 'document'
            elif 'zip' in mime or 'rar' in mime or 'archive' in mime:
                file_obj.file_type = 'archive'
            
            file_obj.save()
            messages.success(request, f'File "{file_obj.filename}" uploaded successfully!')
            return redirect('filesharing:files-list')
        else:
            messages.error(request, 'Error uploading file')
            return redirect('filesharing:files-list')
    else:
        form = FileUploadForm()
    
    context = {
        'form': form,
        'title': 'Upload File',
    }
    return render(request, 'files/upload.html', context)


@login_required
def file_detail(request, pk):
    """View file details and share options"""
    file_obj = get_object_or_404(File, id=pk)
    
    # Check permissions
    if file_obj.owner != request.user and not FileShare.objects.filter(file=file_obj, shared_with_user=request.user, is_active=True).exists():
        messages.error(request, 'You do not have permission to view this file')
        return redirect('filesharing:files-list')
    
    # Get shares and comments
    shares = file_obj.shares.filter(is_active=True)
    comments = file_obj.comments.all().order_by('-created_at')
    
    # Get all users except current user for sharing dropdown
    users = User.objects.exclude(id=request.user.id)
    
    comment_form = FileCommentForm()
    
    # Handle comment submission
    if request.method == 'POST':
        # Check if this is a comment submission
        if 'submit_comment' in request.POST:
            comment_form = FileCommentForm(request.POST)
            if comment_form.is_valid():
                try:
                    comment = comment_form.save(commit=False)
                    comment.file = file_obj
                    comment.user = request.user
                    comment.save()
                    messages.success(request, '✓ Comment added successfully!')
                    return redirect('filesharing:file-detail', pk=pk)
                except Exception as e:
                    messages.error(request, f'Error adding comment: {str(e)}')
            else:
                for field, errors in comment_form.errors.items():
                    for error in errors:
                        messages.error(request, f'Comment error: {error}')
    
    context = {
        'file': file_obj,
        'shares': shares,
        'comments': comments,
        'comment_form': comment_form,
        'is_owner': file_obj.owner == request.user,
        'users': users,
        'title': file_obj.filename,
    }
    return render(request, 'files/detail.html', context)


@login_required
@require_http_methods(['POST'])
def share_file(request, pk):
    """Share a file with another user"""
    file_obj = get_object_or_404(File, id=pk)
    
    # Check ownership
    if file_obj.owner != request.user:
        return HttpResponseForbidden('You can only share your own files')
    
    # Get form data
    shared_with_user_id = request.POST.get('shared_with_user', '').strip()
    permission_level = request.POST.get('permission_level', 'download').strip()
    expires_at = request.POST.get('expires_at', '').strip()
    
    # Validate required fields
    if not shared_with_user_id:
        messages.error(request, 'Please select a user to share with')
        return redirect('filesharing:file-detail', pk=pk)
    
    if not permission_level:
        messages.error(request, 'Please select a permission level')
        return redirect('filesharing:file-detail', pk=pk)
    
    try:
        # Get the user to share with
        share_with_user = User.objects.get(id=int(shared_with_user_id))
        
        # Check if already shared
        existing_share = FileShare.objects.filter(
            file=file_obj,
            shared_with_user=share_with_user,
            is_active=True
        ).first()
        
        if existing_share:
            messages.warning(request, f'File is already shared with {share_with_user.username}')
            return redirect('filesharing:file-detail', pk=pk)
        
        # Check if trying to share with self
        if share_with_user == request.user:
            messages.error(request, 'You cannot share a file with yourself')
            return redirect('filesharing:file-detail', pk=pk)
        
        # Parse expiry date if provided
        expires_at_dt = None
        if expires_at:
            try:
                expires_at_dt = datetime.fromisoformat(expires_at)
            except:
                messages.warning(request, 'Invalid expiry date format. Sharing without expiry.')
        
        # Create the share
        share = FileShare.objects.create(
            file=file_obj,
            shared_with_user=share_with_user,
            permission_level=permission_level,
            expires_at=expires_at_dt,
            is_active=True
        )
        
        messages.success(request, f'✓ File shared with {share_with_user.username}!')
        
    except User.DoesNotExist:
        messages.error(request, 'Selected user not found')
    except ValueError as e:
        messages.error(request, f'Invalid user ID: {str(e)}')
    except Exception as e:
        messages.error(request, f'Error sharing file: {str(e)}')
    
    return redirect('filesharing:file-detail', pk=pk)


@login_required
@require_http_methods(['POST'])
def revoke_share(request, file_pk, share_pk):
    """Revoke file share"""
    file_obj = get_object_or_404(File, id=file_pk)
    
    if file_obj.owner != request.user:
        return HttpResponseForbidden('Only file owner can revoke shares')
    
    share = get_object_or_404(FileShare, id=share_pk, file=file_obj)
    share.delete()
    messages.success(request, 'Share revoked!')
    
    return redirect('filesharing:file-detail', pk=file_pk)


@login_required
def download_file(request, pk):
    """Download a file"""
    file_obj = get_object_or_404(File, id=pk)
    
    # Check permissions
    is_owner = file_obj.owner == request.user
    is_shared = FileShare.objects.filter(
        file=file_obj,
        shared_with_user=request.user,
        is_active=True,
        permission_level='download'
    ).exists()
    is_public = file_obj.is_public
    
    if not (is_owner or is_shared or is_public):
        messages.error(request, 'You do not have permission to download this file')
        return redirect('filesharing:files-list')
    
    # Increment download count
    file_obj.download_count += 1
    file_obj.save()
    
    # Return file download
    from django.http import FileResponse
    response = FileResponse(file_obj.file.open('rb'), as_attachment=True, filename=file_obj.filename)
    return response


@login_required
@require_http_methods(['POST'])
def delete_file(request, pk):
    """Delete a file"""
    file_obj = get_object_or_404(File, id=pk)
    
    if file_obj.owner != request.user:
        return HttpResponseForbidden('You can only delete your own files')
    
    filename = file_obj.filename
    file_obj.file.delete()
    file_obj.delete()
    messages.success(request, f'File "{filename}" deleted successfully!')
    
    return redirect('filesharing:files-list')


@login_required
def shared_files(request):
    """List files shared with current user"""
    user = request.user
    shares = FileShare.objects.filter(shared_with_user=user, is_active=True)
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(shares, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'shares': page_obj.object_list,
        'title': 'Files Shared With Me',
    }
    return render(request, 'files/shared.html', context)


@login_required
def api_file_comments(request, pk):
    """API endpoint to get file comments as JSON"""
    file_obj = get_object_or_404(File, id=pk)
    
    # Check permissions
    if file_obj.owner != request.user and not FileShare.objects.filter(file=file_obj, shared_with_user=request.user, is_active=True).exists():
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    # Get comments
    comments = file_obj.comments.all().order_by('-created_at')
    
    # Format comments for JSON
    comments_data = []
    for comment in comments:
        # Calculate time difference
        time_diff = timezone.now() - comment.created_at
        if time_diff.days > 0:
            time_ago = f"{time_diff.days}d ago"
        elif time_diff.seconds > 3600:
            time_ago = f"{time_diff.seconds // 3600}h ago"
        elif time_diff.seconds > 60:
            time_ago = f"{time_diff.seconds // 60}m ago"
        else:
            time_ago = "just now"
        
        comments_data.append({
            'id': str(comment.id),
            'user': comment.user.username,
            'comment': comment.comment,
            'time_ago': time_ago,
            'created_at': comment.created_at.isoformat()
        })
    
    return JsonResponse({
        'file_id': str(file_obj.id),
        'comments': comments_data,
        'total': len(comments_data)
    })
