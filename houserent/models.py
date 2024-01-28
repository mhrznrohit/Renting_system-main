from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils import timezone

class FlatsAvailable(models.Model):

    uid=models.ForeignKey(User, verbose_name="User Id", on_delete=models.CASCADE,default=6)
    title = models.CharField(max_length=100)
    full_name=models.CharField(max_length=50,null=True)
    email=models.EmailField(max_length=254,null=True)
    phone=models.IntegerField(null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=200,)
    bedroom = models.PositiveIntegerField()
    livingroom = models.PositiveIntegerField()
    bathroom = models.PositiveIntegerField()
    kitchen = models.PositiveIntegerField()
    contact_number = models.CharField(max_length=15)
    date_and_time=models.DateTimeField(default=timezone.now)
    # For multiple images, we can use Django's FileField with the 'upload_to' parameter to specify the upload directory.
    images = models.ImageField(upload_to='uploads',null=True)
    slugs=models.SlugField(unique=True,null=True)


    def __str__(self):
        return self.title
    
@receiver(pre_save, sender=FlatsAvailable)
def generate_slug(sender, instance, **kwargs):
    if not instance.slugs:
        instance.slugs = slugify(instance.title)

# class Bookings(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     flat = models.ForeignKey('FlatsAvailable', on_delete=models.CASCADE)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     persons = models.PositiveIntegerField()
#     profession = models.CharField(max_length=100)
#     relation = models.CharField(max_length=100)
#     date_and_time=models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return f"Booking for {self.user.username} - {self.flat.title}"
    

# class Booked(models.Model):
#     Booking_status=[
#         ('r','requested'),
#         ('a','approved'),
#         ('s','successful'),
#         ('x','rejected')
#     ]
#     flat_id = models.ForeignKey(Bookings, on_delete=models.CASCADE)
#     booked_user=models.CharField(max_length=50,null=True)
#     status=models.CharField(max_length=50,choices=Booking_status,default='r')


#     def __str__(self):
#         return f"Booking {self.id} "

class Flat(models.Model):
    name = models.CharField(max_length=255)
    # other fields for flat details



class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flat = models.OneToOneField(FlatsAvailable, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return f"Booking {self.id}"


    

