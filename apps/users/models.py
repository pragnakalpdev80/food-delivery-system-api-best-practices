from django.db import models
from django.contrib.auth.models import AbstractUser
from common.models.soft_delete import SoftDeleteModel
from common.models.timestamped import TimestampedModel

class User(AbstractUser, TimestampedModel, SoftDeleteModel):
   """ Custom User Model """
   USER_TYPE_CHOICES = (
        ('customer',"Customer"),('restaurant_owner',"Restaurant Owner"),('delivery_driver',"Delivery Driver"),
    )
   email = models. EmailField(unique=True)
   phone_no = models.CharField(max_length = 10,unique=True)
   user_type = models.CharField(choices=USER_TYPE_CHOICES)

   USERNAME_FIELD = 'email'
   REQUIRED_FIELDS = ['phone_no']
   
   def __str__(self):
       return f"{self.username} ({self.user_type})"


class Address(TimestampedModel, SoftDeleteModel):
    """ Customer Address Model """
    address_name = models.CharField(max_length=60)
    address = models.TextField()
    is_default = models.BooleanField(default=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def save(self,*args,**kwargs):
        """ If user creates a new default address then rest of user's address will be removed from the default address. """
        if self.is_default:
            user_address = Address.objects.filter(user=self.user)
            user_address.update(is_default=False)
        super().save(*args,**kwargs)

    def __str__(self):
        return f"{self.user} - {self.address}"


class CustomerProfile(TimestampedModel, SoftDeleteModel):
    """ Customer Profile Model """
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='customer_profile')
    avatar = models.ImageField(default='default.jpg', upload_to='customer_avatar')
    # default_address = models.TextField()
    # saved_addresses = models.JSONField()
    total_orders = models.IntegerField(default=0)
    loyalty_points = models.IntegerField(default=0)

    @property
    def default_address(self):
        user_default_adress = Address.objects.filter(user=self.user, is_default=True).first()
        return user_default_adress

    @property
    def saved_addresses(self):
        user_saved_addresses = Address.objects.filter(user=self.user)
        return user_saved_addresses
    
    def __str__(self):
       return f"{self.user}"


class DriverProfile(TimestampedModel, SoftDeleteModel):
    """ Driver Profile Model """
    VEHICLE_CHOICES = (
        ('bike',"Bike"),('scooter',"Scooter"),('car',"Car"),
    )   

    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='driver_profile')
    avatar = models.ImageField(default='default.jpg', upload_to='driver_avatar')
    vehicle_type = models.CharField(max_length=10,choices=VEHICLE_CHOICES)
    vehicle_number = models.CharField(max_length=10)
    license_number =  models.CharField(max_length=10)
    is_available = models.BooleanField(default=True)
    total_deliveries = models.IntegerField(default=0)
    average_rating  = models.DecimalField(default=0,max_digits=3 ,decimal_places=2)

    def __str__(self):
       return "{}".format(self.user)

    def update_availability(self, status):
        self.is_available = status
        self.save(update_fields=['is_available', 'updated_at'])

    def get_delivery_stats(self):
        return {
            'total_deliveries': self.total_deliveries,
            'average_rating': self.average_rating,
        }
