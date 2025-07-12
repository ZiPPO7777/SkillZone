from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, FeedPost

# Customize how CustomUser appears in the admin
class CustomUserAdmin(UserAdmin):
    # Fields to display in the list view
    list_display = ('username', 'email', 'fullname', 'phone_no', 'is_staff')
    
    # Fieldsets for the edit view
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('fullname', 'email', 'phone_no', 'profile_pic')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Fields when adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'fullname', 'phone_no'),
        }),
    )
    
    # Search and filter options
    search_fields = ('username', 'email', 'fullname', 'phone_no')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

# Register CustomUser with the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)

# Customize FeedPost admin
class FeedPostAdmin(admin.ModelAdmin):
    list_display = ('author', 'caption_preview', 'created_at', 'like_count')
    list_filter = ('created_at', 'author')
    search_fields = ('caption', 'author__username')
    date_hierarchy = 'created_at'
    
    def caption_preview(self, obj):
        return obj.caption[:50] + '...' if obj.caption else ''
    caption_preview.short_description = 'Caption Preview'
    
    def like_count(self, obj):
        return obj.likes.count()
    like_count.short_description = 'Likes'

# Register FeedPost with the custom admin class
admin.site.register(FeedPost, FeedPostAdmin)