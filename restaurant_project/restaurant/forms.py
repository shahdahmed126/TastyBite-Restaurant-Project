import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Order, MenuItem, Reservation


# Shared Bootstrap-style widget classes so the form keeps the site's look
DARK_INPUT = {
    'class': 'form-control form-control-lg border-secondary text-white rounded-3',
    'style': 'background: rgba(11, 15, 25, 0.8);',
}
DARK_TEXTAREA = {
    'class': 'form-control border-secondary text-white rounded-3',
    'style': 'background: rgba(11, 15, 25, 0.8);',
    'rows': 2,
}
DARK_SELECT = {
    'class': 'form-select form-select-lg border-secondary text-white rounded-3',
    'style': 'background: rgba(11, 15, 25, 0.8);',
}


class CheckoutForm(forms.ModelForm):
    """Customer information form used at checkout, with server-side validation."""

    customer_name = forms.CharField(
        label="Full Name",
        max_length=150,
        min_length=3,
        required=True,
        widget=forms.TextInput(attrs={**DARK_INPUT, 'placeholder': 'Mohamed Ellithy'}),
        error_messages={
            'required': 'Please enter your full name.',
            'min_length': 'Name must be at least 3 characters long.',
        },
    )
    phone = forms.CharField(
        label="Phone Number",
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={**DARK_INPUT, 'placeholder': '+20 100 123 4567'}),
        error_messages={'required': 'Please enter a phone number.'},
    )
    address = forms.CharField(
        label="Delivery Address",
        required=False,
        widget=forms.Textarea(attrs={**DARK_TEXTAREA, 'placeholder': 'Street, Building No, Apartment No...'}),
    )
    table_number = forms.CharField(
        label="Table Number",
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={**DARK_INPUT, 'placeholder': 'Table #5'}),
    )
    special_instructions = forms.CharField(
        label="Special Instructions",
        required=False,
        widget=forms.Textarea(attrs={**DARK_TEXTAREA, 'placeholder': 'No mayo, extra spicy, extra napkins...'}),
    )

    class Meta:
        model = Order
        fields = [
            'customer_name', 'phone', 'address', 'order_type',
            'table_number', 'special_instructions', 'payment_method',
        ]
        widgets = {
            'order_type': forms.RadioSelect,
            'payment_method': forms.RadioSelect,
        }

    def clean_phone(self):
        phone = self.cleaned_data['phone'].strip()
        digits_only = re.sub(r'[^\d]', '', phone)
        if len(digits_only) < 8:
            raise forms.ValidationError("Please enter a valid phone number (at least 8 digits).")
        if not re.match(r'^[\d\s\+\-\(\)]+$', phone):
            raise forms.ValidationError("Phone number contains invalid characters.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        order_type = cleaned_data.get('order_type')
        address = cleaned_data.get('address', '').strip() if cleaned_data.get('address') else ''
        table_number = cleaned_data.get('table_number', '').strip() if cleaned_data.get('table_number') else ''

        if order_type == 'DINE_IN':
            if not table_number:
                self.add_error('table_number', 'Please enter your table number for dine-in orders.')
        else:
            if not address:
                self.add_error('address', 'Please enter a delivery/pickup address.')

        return cleaned_data


class MenuItemForm(forms.ModelForm):
    """Used to create and edit menu items, including uploaded photos."""

    class Meta:
        model = MenuItem
        fields = [
            'name', 'name_ar', 'category', 'price',
            'description', 'description_ar',
            'image_upload', 'image',
            'calories', 'prep_time_mins',
            'is_popular', 'is_spicy', 'is_vegetarian', 'rating',
        ]
        widgets = {
            'name': forms.TextInput(attrs=DARK_INPUT),
            'name_ar': forms.TextInput(attrs=DARK_INPUT),
            'category': forms.Select(attrs=DARK_SELECT),
            'price': forms.NumberInput(attrs={**DARK_INPUT, 'step': '0.01'}),
            'description': forms.Textarea(attrs=DARK_TEXTAREA),
            'description_ar': forms.Textarea(attrs=DARK_TEXTAREA),
            'image': forms.URLInput(attrs={
                'class': 'form-control border-secondary text-white rounded-3',
                'style': 'background: rgba(11, 15, 25, 0.8);',
                'placeholder': 'https://images.unsplash.com/...',
            }),
            'image_upload': forms.ClearableFileInput(attrs={
                'class': 'form-control border-secondary text-white rounded-3',
                'style': 'background: rgba(11, 15, 25, 0.8);',
            }),
            'calories': forms.NumberInput(attrs=DARK_INPUT),
            'prep_time_mins': forms.NumberInput(attrs=DARK_INPUT),
            'rating': forms.NumberInput(attrs={**DARK_INPUT, 'step': '0.1', 'min': '0', 'max': '5'}),
        }

    def clean_price(self):
        price = self.cleaned_data['price']
        if price is None or price <= 0:
            raise forms.ValidationError("Price must be greater than 0.")
        return price

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        image_upload = cleaned_data.get('image_upload')
        if not image and not image_upload:
            raise forms.ValidationError("Please provide a dish photo: either upload an image or paste an image URL.")
        return cleaned_data


class ReservationForm(forms.ModelForm):
    """Table booking form with validation."""

    class Meta:
        model = Reservation
        fields = [
            'customer_name', 'phone', 'email',
            'guests_count', 'reservation_date', 'reservation_time',
            'special_requests',
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs=DARK_INPUT),
            'phone': forms.TextInput(attrs=DARK_INPUT),
            'email': forms.EmailInput(attrs=DARK_INPUT),
            'guests_count': forms.NumberInput(attrs={**DARK_INPUT, 'min': '1', 'max': '20'}),
            'reservation_date': forms.DateInput(attrs={**DARK_INPUT, 'type': 'date'}),
            'reservation_time': forms.TimeInput(attrs={**DARK_INPUT, 'type': 'time'}),
            'special_requests': forms.Textarea(attrs=DARK_TEXTAREA),
        }

    def clean_phone(self):
        phone = self.cleaned_data['phone'].strip()
        digits_only = re.sub(r'[^\d]', '', phone)
        if len(digits_only) < 8:
            raise forms.ValidationError("Please enter a valid phone number (at least 8 digits).")
        return phone

    def clean_guests_count(self):
        guests = self.cleaned_data['guests_count']
        if guests < 1:
            raise forms.ValidationError("You need at least 1 guest to make a reservation.")
        if guests > 20:
            raise forms.ValidationError("For parties larger than 20, please call us directly.")
        return guests


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Your username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'you@example.com'}),
        }
