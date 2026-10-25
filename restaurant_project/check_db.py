import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_proj.settings')
django.setup()
from restaurant.models import Category, MenuItem

print('=== DATABASE STATUS ===')
print(f'Categories: {Category.objects.count()}')
print(f'Total Items: {MenuItem.objects.count()}')
print(f'Popular Items: {MenuItem.objects.filter(is_popular=True).count()}')

drinks_count = MenuItem.objects.filter(category__name__in=['Craft Drinks', 'Hot Beverages', 'Fresh Juices']).count()
print(f'Drinks (all types): {drinks_count}')
print(f'Desserts: {MenuItem.objects.filter(category__name="Heavenly Desserts").count()}')

print()
print('=== ALL CATEGORIES ===')
for cat in Category.objects.all():
    print(f'  [{cat.order}] {cat.name}: {cat.items.count()} items')

print()
print('=== POPULAR ITEMS (first 6) ===')
for item in MenuItem.objects.filter(is_popular=True)[:6]:
    print(f'  - {item.name} | {item.price} EGP | Rating: {item.rating}')
