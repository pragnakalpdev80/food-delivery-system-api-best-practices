import uuid
from django.db import models
from common.models.timestamped import TimestampedModel
from apps.users.models import CustomerProfile,Address,DriverProfile
from apps.restaurants.models import Restaurant,MenuItem

class Cart(TimestampedModel):
    """ Cart Model """
    customer = models.OneToOneField(CustomerProfile, on_delete=models.CASCADE, related_name="cart")
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE,related_name="carts",null=True,blank=True,db_index=True)
        
    def __str__(self):
        return f"{self.customer} : {self.restaurant}"
    
    def get_total(self):
        """ method to get total amount of the cart. """
        total = sum(item.get_subtotal() for item in self.cart_items.all())
        return total
    
class CartItem(TimestampedModel):
    """ Cart Items Model """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    menu_item = models.ForeignKey(MenuItem,on_delete=models.CASCADE,related_name='added_item')
    quantity = models.PositiveIntegerField()
    special_instructions = models.TextField(null=True)

    def get_subtotal(self):
        """ Method to get subtotal of cart items. """
        return self.menu_item.price * self.quantity
   
    def __str__(self):
        return f"{self.cart.customer} : {self.menu_item} - {self.quantity}"


class Order(TimestampedModel):
    """ Order Model """
    STATUS_CHOICES = (
        ("pending","Pending"), ("confirmed","Confirmed"), ("preparing","Preparing"), ("ready","Ready"), 
        ("picked_up","Picked Up"), ("delivered","Delivered"), ("cancelled","Cancelled")
    )

    customer =  models.ForeignKey(CustomerProfile,on_delete=models.CASCADE,related_name="order",db_index=True)
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE,related_name="orders",db_index=True)
    driver = models.ForeignKey(DriverProfile,on_delete=models.CASCADE,null=True)
    order_number =models.UUIDField(default=uuid.uuid4)
    status = models.CharField(choices=STATUS_CHOICES,db_index=True)
    delivery_address = models.ForeignKey(Address, on_delete=models.PROTECT)
    subtotal = models.DecimalField(max_digits=10 ,decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=10 ,decimal_places=2)
    tax = models.DecimalField(max_digits=10 ,decimal_places=2)
    total_amount = models.DecimalField(max_digits=10 ,decimal_places=2)
    special_instructions = models.TextField(null=True)
    estimated_delivery_time = models.DateTimeField(null=True)
    actual_delivery_time = models.DateTimeField(null=True)

    def __str__(self):
       return f"{self.order_number}"
    
    def calculate_total(self):
        """ Method to calculate total amount of the cart. """
        return self.subtotal+self.delivery_fee+self.tax
    
    def can_cancel(self):
        """ Method to check order is cancallable or not. """
        return self.status in ['pending', 'confirmed']
           
    def is_delivered(self):
        """ Method to check the order is delivered or not. """
        return self.status == 'delivered'
    
    class Meta:
        indexes = [
            models.Index(fields=['customer', 'status']),
            models.Index(fields=['restaurant', 'status']),
            models.Index(fields=['driver', 'status']),
            models.Index(fields=['customer', '-created_at']),
        ]


class OrderItem(models.Model):
    """ Orders Items Model """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='menu_item')
    menu_item = models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10 ,decimal_places=2)
    special_instructions = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)

    def __str__(self):
       return f"{self.menu_item}: {self.order.customer}"


class Review(TimestampedModel):
    """ Orders Review Model """
    customer = models.ForeignKey(CustomerProfile,on_delete=models.CASCADE,db_index=True, related_name='review')
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE,null=True,db_index=True)
    menu_item = models.ForeignKey(MenuItem,on_delete=models.CASCADE,null=True)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField(null=True)

    def __str__(self):
       return f"{self.customer}: {self.order}: {self.rating}"
    
    class Meta:
        indexes = [
                models.Index(fields=['customer', 'restaurant']),
            ]