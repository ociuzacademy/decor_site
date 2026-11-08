from django.db import models

# Feedback model
class Feedback(models.Model):
    RATING_CHOICES = [
        (1, 'Poor'),
        (2, 'Fair'),
        (3, 'Good'),
        (4, 'Very Good'),
        (5, 'Excellent'),
    ]
    name = models.CharField(max_length=100, blank=True, null=True)
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    comment = models.TextField()

    def __str__(self):
        return f"Feedback from {self.name or 'Anonymous'} - Rating: {self.rating}"

# Register model


# Admin model
class Admin(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=255)  # Plain text password (Not recommended)

    def __str__(self):
        return self.email
# Product model
from django.db import models

class Register(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=255)  # Plain text password (Not recommended)
    address = models.TextField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    delivery_date = models.DateField(blank=True, null=True)  # Add delivery date field

    def __str__(self):
        return self.name

from django.db import models


class Cart(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)



class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        related_name='items',
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
    

from django.db import models
from .models import CartItem
class Order(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Paid', 'Paid')
        ],
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )

    quantity = models.PositiveIntegerField(default=1)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    @property
    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


from django.db import models
from .models import Order, Register

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('CARD', 'Card Payment'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)  # For card payment
    cardholder_name = models.CharField(max_length=255, blank=True, null=True)  # For card payment
    card_number = models.CharField(max_length=20, blank=True, null=True)  # For card payment (masked)
    cvv = models.CharField(max_length=4, blank=True, null=True)  # For card payment
    expiry_date = models.CharField(max_length=5, blank=True, null=True)  # For card payment
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order #{self.order.id} by {self.user.username}"


# models.py
from django.db import models

class Notification(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # To mark whether the admin has read the notification

    def __str__(self):
        return f"Notification for {self.product.name}"

# models.py
from django.db import models
# Assuming you are using Django's default User model

class BuyNow(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"BuyNow - {self.product.name} by {self.user.name}"

from django.db import models

class Payment_buy_now(models.Model):

    PAYMENT_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('CARD', 'Card Payment'),
    ]

    buy_now = models.ForeignKey(
        BuyNow,
        on_delete=models.PROTECT,
        related_name='payments'
    )

    user = models.ForeignKey(Register, on_delete=models.CASCADE)

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES
    )

    transaction_id = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    cardholder_name = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    card_number = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for order {self.buy_now.id}"

from django.db import models
  # Assuming you're using Django's default User model

class TNotification(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()  # The content of the notification
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when notification was created
    is_read = models.BooleanField(default=False)  # Flag to check if the user has read the notification

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:50]}"  # Preview the message
    
    # Optionally, you can add a method to mark as read
    def mark_as_read(self):
        self.is_read = True
        self.save()


from django.db import models
class Category(models.Model):
    category=models.CharField(max_length=100,default='')


class Design(models.Model):
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='design/')  # Image to be uploaded
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField(default=0)  # How many times this design can be booked
    is_available = models.BooleanField(default=True)  # Whether this design is available for booking
    delivery_date = models.DateField(blank=True, null=True)  # Optional delivery date field
    def __str__(self):
        return self.name
    
class Booking(models.Model):
    design = models.ForeignKey(Design, on_delete=models.CASCADE)
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
