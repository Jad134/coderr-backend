from django.contrib import admin
from .models import CustomUser, Review
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Review)

