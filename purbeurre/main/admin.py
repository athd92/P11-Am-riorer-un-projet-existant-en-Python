from django.contrib import admin
from tinymce.widgets import TinyMCE
from main.models import Aliment, Favorite

admin.site.register(Aliment)
admin.site.register(Favorite)