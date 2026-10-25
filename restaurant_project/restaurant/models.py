from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=100)
    name_ar = models.CharField(max_length=100, blank=True, null=True)
    icon = models.CharField(max_length=50, default='fa-bowl-food', help_text="FontAwesome icon class")
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=200)
    name_ar = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField()
    description_ar = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.URLField(max_length=500, blank=True, null=True, help_text="Image URL (used if no uploaded image is provided)")
    image_upload = models.ImageField(upload_to='menu_items/', blank=True, null=True, help_text="Upload a dish photo from your device")
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5.0)
    is_popular = models.BooleanField(default=False)
    is_spicy = models.BooleanField(default=False)
    is_vegetarian = models.BooleanField(default=False)
    calories = models.PositiveIntegerField(default=450)
    prep_time_mins = models.PositiveIntegerField(default=20)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    @property
    def display_image(self):
        """Prefer an uploaded image file; fall back to the image URL."""
        if self.image_upload:
            try:
                return self.image_upload.url
            except ValueError:
                pass
        return self.image or ''


class CustomerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_profile')
    points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.points} points"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_profile(sender, instance, created, **kwargs):
    if created:
        CustomerProfile.objects.create(user=instance)


class Order(models.Model):
    ORDER_TYPE_CHOICES = (
        ('DELIVERY', '🛵 Delivery / توصيل'),
        ('DINE_IN', '🍽️ Dine-In / داخل المطعم'),
        ('TAKEAWAY', '🛍️ Takeaway / استلام'),
    )

    STATUS_CHOICES = (
        ('PENDING', '📥 Order Received / تم الاستلام'),
        ('PREPARING', '👨‍🍳 Preparing / جاري التحضير'),
        ('OUT_FOR_DELIVERY', '🛵 Out for Delivery / في الطريق'),
        ('DELIVERED', '✅ Delivered / تم التسليم'),
        ('CANCELLED', '❌ Cancelled / ملغي'),
    )

    PAYMENT_CHOICES = (
        ('CASH', '💵 Cash on Delivery / كاش'),
        ('CARD', '💳 Credit Card / كارت'),
        ('VODAFONE', '📱 Vodafone Cash / فودافون كاش'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    customer_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True, null=True)
    order_type = models.CharField(max_length=20, choices=ORDER_TYPE_CHOICES, default='DELIVERY')
    table_number = models.CharField(max_length=20, blank=True, null=True)
    special_instructions = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='CASH')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    points_awarded = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    notes = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name} (Order #{self.order.id})"


class Reservation(models.Model):
    STATUS_CHOICES = (
        ('CONFIRMED', 'Confirmed / مؤكد'),
        ('PENDING', 'Pending / قيد الانتظار'),
        ('CANCELLED', 'Cancelled / ملغي'),
    )

    customer_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    guests_count = models.PositiveIntegerField(default=2)
    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    special_requests = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='CONFIRMED')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-reservation_date', '-reservation_time']

    def __str__(self):
        return f"Reservation for {self.customer_name} ({self.guests_count} guests)"
