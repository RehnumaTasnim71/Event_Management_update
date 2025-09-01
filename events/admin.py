from django.contrib import admin
from .models import Event, Category

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date')
    search_fields = ('title',)
    list_filter = ('category', 'date')

admin.site.register(Category)
