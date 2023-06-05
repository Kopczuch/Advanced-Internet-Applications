from django.contrib import admin
from .models import *

admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(Image)
# admin.site.register(EmbeddedVideoItem)