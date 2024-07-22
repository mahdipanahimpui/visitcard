from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator
from functools import partial
from django.core.exceptions import ValidationError


# -------------------------------------- FUNCTIONS ---------------------------------------------
def validate_max_file_size(value, max_size):
    # max_size = 10 * 1024 * 1024
    if value.size > max_size:
        raise ValidationError(f"The file size should not exceed {max_size} bytes.")


# -------------------------------------- MODELS ---------------------------------------------
class Page(models.Model):

    PUBLISH_CHOICES = (
        ('public', 'public'),
        ('private', 'private'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    banner_image = models.ImageField(upload_to='upload/image/', null=True, blank=True,
                                        validators=[
        partial(validate_max_file_size, max_size=10 * 1024 * 1024),
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
    ])

    logo_image = models.ImageField(upload_to='upload/image/', null=True, blank=True,
                                    validators=[
        partial(validate_max_file_size, max_size=5 * 1024 * 1024),
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
    ])

    qr_code = models.ImageField(upload_to='uploads/image/', 
                                    validators=[
        partial(validate_max_file_size, max_size=5 * 1024 * 1024),
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
    ])

    cv = models.FileField(upload_to='uploads/file/', null=True, blank=True,
                                    validators=[
        partial(validate_max_file_size, max_size=10 * 1024 * 1024),
        FileExtensionValidator(allowed_extensions=['pdf']),
    ])

    identification = models.CharField(max_length=128, unique=True)


    title = models.CharField(max_length=128)
    subject = models.CharField(max_length=128, blank=True, null=True)
    description = models.TextField(max_length=1024)

    max_address_count = models.SmallIntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(20)])
    max_image_count = models.SmallIntegerField(default=3,  validators=[MinValueValidator(0), MaxValueValidator(20)])
    max_comminucation_count = models.PositiveSmallIntegerField(default=10, validators=[MinValueValidator(20)])

    publish = models.CharField(default='public', max_length=30, choices=PUBLISH_CHOICES)
    slug = models.SlugField(default="", null=True, blank=True)
    is_active_by_admin = models.BooleanField(default=True)
    is_active_by_user = models.BooleanField(default=True)
    is_premium = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Image(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, null=True, blank=True)
    image = models.ImageField(upload_to='upload/image/')



class Comminucation(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    PLATFORM_CHOICES = (
        ('phone', 'phone'),
        ('instagram', 'instagram'),
        ('telegram', 'telegram'),
        ('whatsapp', 'whatsapp'),
        ('eitaa', 'eitaa'),
        ('rubika', 'rubika'),
        ('bale', 'bale'),
        ('gap', 'gap'),
        ('igap', 'igap'),
        ('gmail', 'gmail'),
        ('outlook', 'outlook'),
        ('yahoo', 'yahoo'),
        ('email', 'email'),
        ('linkedin', 'linkedin'),
        ('github', 'github'),
        ('website', 'website')
    )
    platform = models.CharField(max_length=30, choices=PLATFORM_CHOICES)
    link = models.CharField(max_length=128)



class Location(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=True, blank=True)
    long = models.DecimalField(max_digits=9, decimal_places=6)
    lat  = models.DecimalField(max_digits=9, decimal_places=6)



class Address(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=True, blank=True)
    address = models.TextField(max_length=1024)



# class PageImageRelation(models.Model):
#     page = models.ForeignKey(Page, on_delete=models.CASCADE)
#     image = models.ForeignKey(Image, on_delete=models.CASCADE)



# class PageComminucationRelation(models.Model):
#     page = models.ForeignKey(Page, on_delete=models.CASCADE)
#     link = models.ForeignKey(Comminucation, on_delete=models.CASCADE)



# class PageLocationRelation(models.Model):
#     page = models.ForeignKey(Page, on_delete=models.CASCADE)
#     location = models.ForeignKey(Location, on_delete=models.CASCADE)




    







