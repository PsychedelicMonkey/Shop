from django.contrib.auth.models import User
from django.db import models
from PIL import Image, ImageOps


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile", null=True, blank=True)
    bio = models.TextField(max_length=100, null=True, blank=True)
    is_private = models.BooleanField(default=True)

    @property
    def image_url(self):
        try:
            return self.image.url
        except ValueError:
            return None

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            img = ImageOps.fit(img, (100, 100))
            img.save(self.image.path)
