from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.postgres.fields import JSONField
import json
from ordered_model.models import OrderedModel
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
import os

def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1]  # Get file extension
    valid_extensions = ['.jpg', '.jpeg', '.png']
    if ext.lower() not in valid_extensions:
        raise ValidationError('Invalid file extension. Please upload a JPEG, PNG, or JPG file.')
class Coupons(models.Model):
    coupon_name=models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    coupon_amount = models.DecimalField(max_digits=10, decimal_places=2)
    for_one_time = models.BooleanField(default=False)  # Default to one-time use
    def __str__(self):
        return self.coupon_name

class UserCoupon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupons, on_delete=models.CASCADE)
    used = models.BooleanField(default=False)
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    order_history = models.TextField(default='[]')  # Default to an empty list as a JSON-formatted string
    def add_order_to_history(self, items, total):
        order_data = {
            'timestamp': timezone.now().isoformat(),
            'items': items,
            'total': total,
        }
        order_history = json.loads(self.order_history)
        order_history.append(order_data)
        self.order_history = json.dumps(order_history)
        self.save()
class Category(OrderedModel):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='categoryimg/', null=True, blank=True)
    class Meta(OrderedModel.Meta):
        pass

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(null=True,max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, null=True,decimal_places=2)
    image = models.ImageField(upload_to='images/', validators=[validate_image_extension], blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    available = models.BooleanField(default=True,null=True)

    def __str__(self):
        return self.name

class FlashOffer(models.Model):
    image = models.ImageField(upload_to='offer/', null=True, blank=True)
    visibility = models.BooleanField(default=True,null=True)
    available = models.BooleanField(default=True,null=True)

class ScrollingText(models.Model):
    text = models.TextField()
    def __str__(self):
        return self.text
class DeliveryCharge(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    mininum_order = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Rs{self.amount}"
class Loading(models.Model):
    gif_file = models.ImageField(upload_to='gifs/')
class WebsiteOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming you have a User model
    invoice = models.AutoField(primary_key=True)  # Autogenerated and increasing invoice number
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    # Order Status Choices
    ORDER_STATUS_CHOICES = (
        (1, 'In'),
        (2, 'Baking'),
        (3, 'Dispatched'),
    )

    order_status = models.IntegerField(choices=ORDER_STATUS_CHOICES)
    total = models.DecimalField(null=True,max_digits=10, decimal_places=2)
    def __str__(self):
        return f"Order {self.invoice}"

class WebsiteItems(models.Model):
    order_link=models.ForeignKey(
        WebsiteOrder, on_delete=models.CASCADE, null=True
    )
    name = models.CharField(max_length=255)
    price = models.DecimalField(null=True,max_digits=10, decimal_places=2)