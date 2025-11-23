from django.urls import path
from . import views

app_name = 'filesharing'

urlpatterns = [
    # Authentication
    path('', views.home, name='home'),
    path('get-started/', views.get_started, name='get-started'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('search/', views.search, name='search'),
    
    # Device Management
    path('devices/', views.devices_list, name='devices-list'),
    path('devices/register/', views.register_device, name='register-device'),
    path('devices/<uuid:pk>/', views.device_detail, name='device-detail'),
    path('devices/<uuid:pk>/edit/', views.edit_device, name='device-edit'),
    path('devices/<uuid:pk>/delete/', views.delete_device, name='device-delete'),
    
    # WiFi Network Management
    path('networks/', views.networks_list, name='networks-list'),
    path('networks/create/', views.create_network, name='network-create'),
    path('networks/<uuid:pk>/', views.network_detail, name='network-detail'),
    path('networks/<uuid:pk>/edit/', views.edit_network, name='network-edit'),
    path('networks/<uuid:pk>/delete/', views.delete_network, name='network-delete'),
    
    # Network Sharing
    path('networks/<uuid:pk>/share/', views.share_network, name='network-share'),
    path('networks/<uuid:network_pk>/share/<uuid:share_pk>/revoke/', views.revoke_share, name='share-revoke'),
    path('networks/shared/', views.shared_networks, name='shared-networks'),
    
    # Network Invitations
    path('networks/<uuid:pk>/invite/', views.send_invitation, name='send-invitation'),
    path('invitations/', views.invitations, name='invitations'),
    path('invitations/<uuid:pk>/accept/', views.accept_invitation, name='accept-invitation'),
    path('invitations/<uuid:pk>/reject/', views.reject_invitation, name='reject-invitation'),
    
    # User Profile
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='profile-edit'),
    
    # File Sharing
    path('files/', views.files_list, name='files-list'),
    path('files/upload/', views.upload_file, name='file-upload'),
    path('files/shared/', views.shared_files, name='shared-files'),
    path('files/<uuid:pk>/', views.file_detail, name='file-detail'),
    path('files/<uuid:pk>/share/', views.share_file, name='file-share'),
    path('files/<uuid:pk>/download/', views.download_file, name='file-download'),
    path('files/<uuid:pk>/delete/', views.delete_file, name='file-delete'),
    path('files/<uuid:file_pk>/share/<uuid:share_pk>/revoke/', views.revoke_share, name='file-share-revoke'),
    
    # API Endpoints
    path('api/network/<uuid:pk>/stats/', views.api_network_stats, name='api-network-stats'),
    path('api/device/<uuid:pk>/status/', views.api_device_status, name='api-device-status'),
    path('api/files/<uuid:pk>/comments/', views.api_file_comments, name='api-file-comments'),
]

