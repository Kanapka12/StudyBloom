import uuid
import os
import random
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.files.storage import default_storage
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


# def random_profile_image():
#     image_folder = 'accounts/default_profile_images'
#     images = default_storage.listdir(image_folder)[1]
#     chosen_image = random.choice(images)
#     print(os.path.join(image_folder, chosen_image))
#     print(type(os.path.join(image_folder, chosen_image)))
#     return os.path.join(image_folder, chosen_image)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='accounts/avatars', default='accounts/avatars/791498.png')
    background_color = models.CharField(max_length=7, default="#357e40")

    # nadpisz stare zdjecie
    # def save(self, *args, **kwargs):
    #     if self.pk is not None:
    #         old_profile_image = CustomUser.objects.get(pk=self.pk).profile_image
    #         if old_profile_image != self.profile_image and old_profile_image != 'default_profile_image.png':
    #             default_storage.delete(old_profile_image.path)
    #     super().save(*args, **kwargs)


class EmailChangeRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    new_email = models.EmailField()
    confirmation_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
