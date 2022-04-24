from django.db import models
import uuid
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
# Create your models here.

class File(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True) 
    title = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True)
    file = models.FileField()


class UserAvatarSerializer(ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
    

    def save(self, *args, **kwargs):
        if self.instance.avatar:
            self.instance.avatar.delete()
        return super().save(*args, **kwargs)



from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    bucket_name = 'www.test-1.com'
    default_acl = "public-read"


class userSerializers(ModelSerializer):
 
    class Meta:
        model = User
        fields =  '__all__'