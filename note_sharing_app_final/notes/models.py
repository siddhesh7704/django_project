from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Signupstd(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    Rollno = models.CharField(max_length=10,null=True)
    branch = models.CharField(max_length=30,null=True)
    year = models.CharField(max_length=10,null=True)
    role = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username

class Signupteach(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    teachID = models.CharField(max_length=10,null=True)
    branch = models.CharField(max_length=30)
    role = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username      

class Notes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    uploadingdate = models.CharField(max_length=30)
    branch = models.CharField(max_length=30)
    subject = models.CharField(max_length=30)
    notesfile = models.FileField(null=True)
    fyletype = models.CharField(max_length=30)
    description = models.CharField(max_length=200,null=True)
    status = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username
