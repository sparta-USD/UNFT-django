import os
from uuid import uuid4
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your models here.
def upload_to_base(instance, filename):
    upload_to = f'unft/base/'
    ext = filename.split('.')[-1]
    uuid = uuid4().hex
    filename = '{}.{}'.format(uuid, ext)
    return os.path.join(upload_to, filename)

def upload_to_style(instance, filename):
    upload_to = f'unft/style/'
    ext = filename.split('.')[-1]
    uuid = uuid4().hex
    filename = '{}.{}'.format(uuid, ext)
    return os.path.join(upload_to, filename)

def upload_to_result(instance, filename):
    upload_to = f'unft/result/'
    ext = filename.split('.')[-1]
    uuid = uuid4().hex
    filename = '{}.{}'.format(uuid, ext)
    return os.path.join(upload_to, filename)

class Unft(models.Model):
    base_image = models.ImageField(upload_to=upload_to_base, max_length=255)
    style_image = models.ImageField(upload_to=upload_to_style, max_length=255)
    result_image = models.ImageField(upload_to=upload_to_result, max_length=255, null=True)
    title = models.CharField(max_length=100)
    desc = models.TextField()
    hits = models.IntegerField(default=0)
    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="create_unft")
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="own_unft")
    status = models.BooleanField(default=False)
    price = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "U-NFT"
        verbose_name = "U-NFT"
        verbose_name_plural = "U-NFT"


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Unft_detail", kwargs={"id": self.id})