from django.contrib import admin
from django.utils.html import format_html
from .models import Device, WiFiNetwork, SharedNetwork, NetworkShare, NetworkInvitation, File, FileShare, FileComment


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_name', 'device_type', 'mac_address', 'status_badge', 'user', 'last_seen')
    list_filter = ('device_type', 'is_online', 'created_at')
    search_fields = ('device_name', 'mac_address', 'ip_address', 'user__username')
    readonly_fields = ('id', 'created_at', 'last_seen')
    fieldsets = (
        ('Device Information', {
            'fields': ('id', 'user', 'device_name', 'device_type', 'mac_address', 'ip_address')
        }),
        ('Status', {
            'fields': ('is_online', 'last_seen', 'created_at')
        }),
    )
    
    def status_badge(self, obj):
        if obj.is_online:
            color = '#28a745'
            status = 'Online'
        else:
            color = '#6c757d'
            status = 'Offline'
        return format_html(
            '<span style="color: {}; font-weight: bold;"><i class="fas fa-circle"></i> {}</span>',
            color,
            status
        )
    status_badge.short_description = 'Status'


@admin.register(WiFiNetwork)
class WiFiNetworkAdmin(admin.ModelAdmin):
    list_display = ('network_name', 'owner', 'security_type', 'frequency_band', 'status_badge', 'connected_count', 'created_at')
    list_filter = ('security_type', 'frequency_band', 'is_active', 'created_at')
    search_fields = ('network_name', 'owner__username', 'password')
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        ('Network Configuration', {
            'fields': ('id', 'owner', 'source_device', 'network_name', 'password')
        }),
        ('Technical Settings', {
            'fields': ('security_type', 'frequency_band', 'channel', 'signal_strength')
        }),
        ('Connection', {
            'fields': ('max_devices', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        if obj.is_active:
            color = '#28a745'
            status = 'Active'
        else:
            color = '#dc3545'
            status = 'Inactive'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            status
        )
    status_badge.short_description = 'Status'
    
    def connected_count(self, obj):
        return f"{obj.connected_devices_count()}/{obj.max_devices}"
    connected_count.short_description = 'Connected'


@admin.register(SharedNetwork)
class SharedNetworkAdmin(admin.ModelAdmin):
    list_display = ('network', 'device', 'is_connected', 'connection_quality', 'last_activity')
    list_filter = ('is_connected', 'connected_at')
    search_fields = ('network__network_name', 'device__device_name')
    readonly_fields = ('id', 'connected_at', 'last_activity')
    fieldsets = (
        ('Connection', {
            'fields': ('id', 'network', 'device', 'is_connected', 'connection_quality')
        }),
        ('Data Usage', {
            'fields': ('data_used',)
        }),
        ('Timestamps', {
            'fields': ('connected_at', 'last_activity')
        }),
    )


@admin.register(NetworkShare)
class NetworkShareAdmin(admin.ModelAdmin):
    list_display = ('network', 'shared_with_user', 'permission_level', 'is_active', 'created_at')
    list_filter = ('permission_level', 'is_active', 'created_at')
    search_fields = ('network__network_name', 'shared_with_user__username')
    readonly_fields = ('id', 'created_at')
    fieldsets = (
        ('Share Information', {
            'fields': ('id', 'network', 'shared_with_user')
        }),
        ('Permissions', {
            'fields': ('permission_level', 'is_active', 'expires_at')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )


@admin.register(NetworkInvitation)
class NetworkInvitationAdmin(admin.ModelAdmin):
    list_display = ('network', 'invited_user', 'invited_by', 'status', 'expires_at')
    list_filter = ('status', 'created_at', 'expires_at')
    search_fields = ('network__network_name', 'invited_user__username', 'invited_by__username')
    readonly_fields = ('id', 'created_at', 'responded_at')
    fieldsets = (
        ('Invitation', {
            'fields': ('id', 'network', 'invited_user', 'invited_by')
        }),
        ('Status', {
            'fields': ('status', 'created_at', 'expires_at', 'responded_at')
        }),
    )


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('filename', 'owner', 'file_type', 'file_size_display', 'is_public', 'download_count', 'created_at')
    list_filter = ('file_type', 'is_public', 'created_at')
    search_fields = ('filename', 'owner__username')
    readonly_fields = ('id', 'created_at', 'updated_at', 'file_size')
    fieldsets = (
        ('File Information', {
            'fields': ('id', 'owner', 'filename', 'file')
        }),
        ('File Details', {
            'fields': ('file_type', 'file_size', 'mime_type')
        }),
        ('Access', {
            'fields': ('is_public', 'download_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def file_size_display(self, obj):
        return obj.get_display_size()
    file_size_display.short_description = 'Size'


@admin.register(FileShare)
class FileShareAdmin(admin.ModelAdmin):
    list_display = ('file', 'shared_with_user', 'permission_level', 'status_badge', 'expires_at', 'created_at')
    list_filter = ('permission_level', 'is_active', 'created_at')
    search_fields = ('file__filename', 'shared_with_user__username')
    readonly_fields = ('id', 'created_at')
    fieldsets = (
        ('Share Information', {
            'fields': ('id', 'file', 'shared_with_user')
        }),
        ('Permissions', {
            'fields': ('permission_level', 'is_active', 'expires_at')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )
    
    def status_badge(self, obj):
        if obj.is_active:
            color = '#28a745'
            status = 'Active'
        else:
            color = '#dc3545'
            status = 'Inactive'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            status
        )
    status_badge.short_description = 'Status'


@admin.register(FileComment)
class FileCommentAdmin(admin.ModelAdmin):
    list_display = ('file', 'user', 'comment_preview', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('file__filename', 'user__username', 'comment')
    readonly_fields = ('id', 'created_at')
    
    def comment_preview(self, obj):
        return obj.comment[:50] + '...' if len(obj.comment) > 50 else obj.comment
    comment_preview.short_description = 'Comment'


