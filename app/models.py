from django.db import models
from django.db.models.signals import pre_save
from core.utils import slug_pre_save_receiver


# Create your models here.

# <editor-fold desc="Gmail model">
class appEmailDataModel(models.Model):
    smtp_id = models.CharField(max_length=100, unique=True)
    from_user = models.EmailField()
    to_user = models.EmailField()
    # cc_users = models.ManyToManyField(blank=True, null=True)
    cc_users = models.CharField(max_length=1024, null=True, blank=True)
    subject = models.CharField(max_length=1024, null=True, blank=True)
    content = models.TextField(null=True, blank=True)  # body
    dir = models.CharField(max_length=100, default="-")
    attachments = models.ImageField(upload_to="attachments", null=True, blank=True)
    received_at = models.DateTimeField(null=True, blank=True)
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.from_user


pre_save.connect(slug_pre_save_receiver, sender=appEmailDataModel)


# </editor-fold>

# <editor-fold desc="Gmail Dir list model">
class appGmailDirModel(models.Model):
    title = models.CharField(max_length=100)
    dir = models.CharField(max_length=100)
    type = models.CharField(max_length=100)

    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


pre_save.connect(slug_pre_save_receiver, sender=appEmailDataModel)


# </editor-fold>

# <editor-fold desc="User gmail smtp Credentials Model">
class appEmailUserCredentialsModel(models.Model):
    email = models.EmailField()
    smtp_password = models.CharField(max_length=100)

    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


pre_save.connect(slug_pre_save_receiver, sender=appEmailUserCredentialsModel)
# </editor-fold>


# class emailTEmailMainModel(models.Model):
#     from_user = models.ManyToManyField(get_user_model(),related_name="emailTEmailMainModel_from_user")
#     to_user = models.ManyToManyField(get_user_model(), related_name="emailTEmailMainModel_to_user")
#     cc_users = models.ManyToManyField(get_user_model(), related_name="emailTEmailMainModel_cc_users")
#     subject = models.CharField(max_length=250)
#     content = models.TextField()
#     attachments = models.ManyToManyField(imageFileMIMainModel,related_name="emailTEmailMainModel_attachments")
#     images = models.ManyToManyField(imageFileMFMainModel,related_name="emailTEmailMainModel_attachments_images")
#     status = models.CharField(max_length=100,choices=emailTEmailMainModelStatusTypeEnumTypes.choices(),default="PENDING")
#
#     slug = models.SlugField(max_length=250, null=True, blank=True, unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#
# pre_save.connect(slug_pre_save_receiver, sender=emailTEmailMainModel)
