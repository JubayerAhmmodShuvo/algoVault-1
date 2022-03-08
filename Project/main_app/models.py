from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(null=True, max_length=256)
    fullName = models.CharField(max_length=50, default="N/A")
    isVarified = models.BooleanField(default=False)
    auth_token = models.CharField(null=True, max_length=200)
    isAdmin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username



class Tutorial(models.Model):
    tag_choices = (
        ('প্রোগ্রামিং বাসিক', 'রোগ্রামিং বাসিক'),
        ('নাম্বার থিওরি', 'নাম্বার থিওরি'),
        ('ডাটা স্ট্রাকচার', 'ডাটা স্ট্রাকচার'),
        ('ডাইনামিক প্রোগ্রামিং', 'ডাইনামিক প্রোগ্রামিং'),
        ('গ্রাফ থিওরি', 'গ্রাফ থিওরি')
    )
    level_choices = (
        (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)
    )
    title = models.CharField(max_length=200, null=True)
    tag = models.CharField(max_length=100, choices=tag_choices)
    level = models.IntegerField(null=True, choices=level_choices)
    content = RichTextField()

    isApproved = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title



class Reading_list(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Tutorial, on_delete=models.CASCADE)



class Topic_Recommendation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    topic1 = models.CharField(max_length=100, null=True, blank=True)
    topic2 = models.CharField(max_length=100, null=True, blank=True)