from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('account/', views.account_view, name='account'),
    path('menu/', views.menu_view, name='menu'),
    path('item/<int:pk>/', views.item_detail_view, name='item_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order-success/<int:order_id>/', views.order_success_view, name='order_success'),
    path('track-order/', views.track_order_view, name='track_order'),
    path('reservation/', views.reservation_view, name='reservation'),
    path('reservation-success/<int:reservation_id>/', views.reservation_success_view, name='reservation_success'),
    path('kitchen-dashboard/', views.kitchen_dashboard_view, name='kitchen_dashboard'),
    path('update-order-status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    
    # Traditional Cart Actions
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:item_id>/<str:action>/', views.update_cart_quantity, name='update_cart_quantity'),
    
    # AJAX Cart Endpoints
    path('api/cart/add/<int:item_id>/', views.add_to_cart_ajax, name='add_to_cart_ajax'),
    path('api/cart/update/<int:item_id>/', views.update_cart_ajax, name='update_cart_ajax'),
    path('api/cart/get/', views.get_cart_ajax, name='get_cart_ajax'),

    # Menu Item CRUD (staff only)
    path('manage-items/', views.manage_items_view, name='manage_items'),
    path('add-item/', views.add_item_view, name='add_item'),
    path('edit-item/<int:pk>/', views.edit_item_view, name='edit_item'),
    path('delete-item/<int:pk>/', views.delete_item_view, name='delete_item'),
]