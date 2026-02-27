from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['hotel', 'user', 'rating', 'short_comment', 'created_at']
    list_filter = ['rating', 'hotel']
    search_fields = ['hotel__name', 'user__email']
    def short_comment(self, obj):
        return obj.comment[:60] + '...' if len(obj.comment) > 60 else obj.comment
    short_comment.short_description = 'Comment'
