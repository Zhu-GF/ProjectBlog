from django.contrib import admin
from app01 import models
# Register your models here.

admin.site.register(models.UserInfo)
admin.site.register(models.Category)
admin.site.register(models.Articles2Tag)
admin.site.register(models.Articles)
admin.site.register(models.Comment)
admin.site.register(models.Blog)
admin.site.register(models.Tag)
admin.site.register(models.Articel_Detail)
admin.site.register(models.UserFans)