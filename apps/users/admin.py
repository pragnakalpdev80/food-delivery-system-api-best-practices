from django.contrib import admin
from .models import (
    User, 
    CustomerProfile, 
    DriverProfile, 
    Address
)
# Register your models here.
admin.site.register(User)
admin.site.register(Address)
admin.site.register(CustomerProfile)
admin.site.register(DriverProfile)
