from re import M
from django.contrib import admin

# Register your models here.
from .models import Move, Set, Session

admin.site.register(Move)
admin.site.register(Set)
admin.site.register(Session)
