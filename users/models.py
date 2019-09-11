from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_unicode_slug
import uuid


class User(AbstractUser):
    GENDER_CHOICE = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=20, unique=True, blank=False, validators=[validate_unicode_slug])
    password = models.CharField(max_length=200, blank=False)
    email = models.EmailField(unique=True, blank=False)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE, blank=False)
    bio = models.TextField(max_length=300)
    email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


class student_list(models.Model):
    name = models.CharField(max_length=200)
    cgpa = models.FloatField()
    id = models.CharField(primary_key=True, blank=False, max_length=100)

    def __str__(self):
        return self.name


class file_list(models.Model):
    file = models.FileField(blank=False, null=False)
    remark = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


class ImageFile(models.Model):
    image = models.ImageField(blank=False, null=False)

    def __str__(self):
        return self.image.name


class category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class quotes(models.Model):
    body = models.TextField()
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    posted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body


# MODIFIED TASKS
from django.conf import settings


def gen_filename(instance, filename):
    return "updates/{user}/{filename}".format(user=instance.user, filename=filename)


class StatusQuerySet(models.QuerySet):
    pass


class StatusManager(models.Manager):
    def get_queryset(self):
        return StatusQuerySet(self.model, using=self._db)


class Status(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=gen_filename, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = StatusManager()

    def __str__(self):
        return str(self.content)[:50]

    class Meta:
        verbose_name = 'Status Post'
        verbose_name_plural = 'Status Posts'


















