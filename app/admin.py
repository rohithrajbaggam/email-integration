from django.contrib import admin
from .models import appEmailDataModel, appEmailUserCredentialsModel, appGmailDirModel
# Register your models here.



admin.site.register(appEmailDataModel)
admin.site.register(appEmailUserCredentialsModel)
admin.site.register(appGmailDirModel)
