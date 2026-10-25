from django.contrib import admin
from .models import Category, MenuItem, Order, OrderItem, Reservation

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'image']
    search_fields = ['name']

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'rating', 'is_popular']
    list_filter = ['category', 'is_popular', 'is_spicy', 'is_vegetarian']
    search_fields = ['name', 'description']
    list_editable = ['price', 'rating', 'is_popular']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['menu_item', 'quantity', 'price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'phone', 'order_type', 'status', 'total_price', 'is_completed', 'created_at']
    list_filter = ['is_completed', 'status', 'order_type', 'payment_method', 'created_at']
    search_fields = ['customer_name', 'phone', 'address']
    list_editable = ['is_completed', 'status']
    inlines = [OrderItemInline]


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'phone', 'guests_count', 'reservation_date', 'reservation_time', 'status']
    list_filter = ['status', 'reservation_date']
    search_fields = ['customer_name', 'phone', 'email']
    list_editable = ['status']