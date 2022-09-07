from django.contrib import admin
from .models import Note, Category

# Register your models here.
admin.site.register(Note)
admin.site.register(Category)