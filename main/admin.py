from django.contrib import admin
from .models import BookFormat, Type, BookClub, Reading, Question, Response, Shelf, JoinClub

# Register your models here.
admin.site.register(BookFormat)
admin.site.register(Type)
admin.site.register(BookClub)
admin.site.register(Reading)
admin.site.register(Question)
admin.site.register(Response)
admin.site.register(Shelf)
admin.site.register(JoinClub)
