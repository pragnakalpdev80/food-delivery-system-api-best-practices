from django.utils import timezone
from django.db import models
from django.db.models import Avg, Count
from apps.users.models import User
from common.models.soft_delete import SoftDeleteModel
from common.models.timestamped import TimestampedModel

class Restaurant(TimestampedModel, SoftDeleteModel):
    """ Restaurant Model """
    CUISINE_CHOICES = (
        ("italian","Italian"), ("chinese","Chinese"), ("indian","Indian"), ("mexican","Mexican"), 
        ("american","American"), ("japanese","Japanese"), ("thai","Thai"), ("mediterranean","Mediterranean")
    )
    owner = models.OneToOneField(User,on_delete=models.CASCADE, related_name="restaurant_owner")
    name = models.CharField(max_length=50)
    description = models.TextField()
    cuisine_type = models.CharField(choices=CUISINE_CHOICES)
    address =models.TextField()
    phone_no = models.CharField(max_length = 10)
    email = models.EmailField()
    logo = models.ImageField(default='default.jpg', upload_to='restaurant_logo')
    banner = models.ImageField(default='default.jpg', upload_to='restaurant_banner')
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    is_open = models.BooleanField(default=False)
    delivery_fee = models.DecimalField(max_digits=10 ,decimal_places=2)
    minimum_order = models.DecimalField(default=0,max_digits=10 ,decimal_places=2)
    average_rating = models.DecimalField(default=0,max_digits=10 ,decimal_places=2)
    total_reviews = models.IntegerField(default=0)

    def __str__(self):
       return "{}".format(self.name)
    
    def is_currently_open(self):
        """ Method to check restaurant is currently open or not. """
        current_time = timezone.localtime(timezone.now()).time()
        return self.opening_time <= current_time <= self.closing_time

    def update_average_rating(self):
        """ Method to update the average rating of restaurant. """
        result = self.review_set.aggregate(avg=Avg('rating'), count=Count('id'))
        self.average_rating = round(result['avg'])
        self.total_reviews = result['count']
        self.save(update_fields=['average_rating', 'total_reviews', 'updated_at'])


class MenuItem(TimestampedModel,SoftDeleteModel):
    """ Restaurants Menu Items Model """
    CATEGORY_CHOICES = (
        ("appetizer","Appetizer"), ("main_course","Main Course"), ("dessert","Dessert"), 
        ("beverage","Beverage"), ("side_dish","Side Dish")
    )

    DIETARY_INFO_CHOICES = (
        ("vegetarian","Vegetarian"), ("vegan","Vegan"), ("gluten_free","Gluten-Free"), 
        ("dairy_free","Dairy-Free"), ("none","None")
    )

    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE,db_index=True,related_name='menu_items')
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10 ,decimal_places=2)
    category = models.CharField(choices=CATEGORY_CHOICES)
    dietary_info = models.CharField(choices=DIETARY_INFO_CHOICES)
    image = models.ImageField(default='default.jpg', upload_to='menu_items')
    is_available = models.BooleanField(default=True)
    preparation_time = models.IntegerField()

    def __str__(self):
       return f"{self.name}"
