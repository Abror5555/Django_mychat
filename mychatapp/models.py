from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    pic = models.ImageField(upload_to="porfile_img/", blank=True, null=True)
    friends = models.ManyToManyField('Friend', related_name="Friend")

    def __str__(self) -> str:
        return self.name
    

class Friend(models.Model):
    profiles = models.OneToOneField(Profile, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.profiles.name
    
class ChatMessage(models.Model):
    body = models.TextField()
    msg_sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="msg_sender")
    msg_receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="msg_receiver")
    seen = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.body