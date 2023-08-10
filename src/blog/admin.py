from django.contrib import admin
from blog.models import BlogPost
from blog.models import Sessions

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'session', 'display_order')
    search_field = ('title', 'session')

    filter_horizontal = ()
    list_filter = ('session',)
    fieldsets = ()
    ordering = ('session', 'display_order') 

class SectionAdmin(admin.ModelAdmin):
    list_display = ('display_order', 'title')
    search_field = ('title')

    filter_horizontal = ()
    fieldsets = ()
    ordering = ('display_order',) 

admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Sessions, SectionAdmin)