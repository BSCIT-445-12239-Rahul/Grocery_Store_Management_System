import re
from django import forms
from django.contrib.auth.models       import User
from django.contrib.auth.forms        import UserCreationForm, AuthenticationForm
from django.core.exceptions           import ValidationError
from .models                          import Product


# ════════════════════════════════════════════════════════
# SHARED VALIDATORS
# ════════════════════════════════════════════════════════

def validate_username(username):
    if len(username) < 4:
        raise ValidationError('Username must be at least 4 characters long.')
    if len(username) > 30:
        raise ValidationError('Username cannot exceed 30 characters.')
    if not re.search(r'[a-zA-Z]', username):
        raise ValidationError('Username must contain at least one letter (a–z or A–Z).')
    if not re.search(r'[0-9]', username):
        raise ValidationError('Username must contain at least one number (0–9). Example: rahul123')
    if not re.match(r'^[a-zA-Z0-9]+$', username):
        raise ValidationError('Username can only contain letters and numbers. No spaces or special characters.')


def validate_name(value, field_label='Name'):
    value = value.strip()
    if len(value) < 2:
        raise ValidationError(f'{field_label} must be at least 2 characters.')
    if len(value) > 50:
        raise ValidationError(f'{field_label} cannot exceed 50 characters.')
    if not re.match(r"^[a-zA-Z\s\-']+$", value):
        raise ValidationError(f'{field_label} can only contain letters, spaces, hyphens, and apostrophes.')


def validate_password_strength(password):
    if len(password) < 8:
        raise ValidationError('Password must be at least 8 characters.')
    if not re.search(r'[A-Z]', password):
        raise ValidationError('Password must contain at least one uppercase letter.')
    if not re.search(r'[0-9]', password):
        raise ValidationError('Password must contain at least one number.')


# ════════════════════════════════════════════════════════
# REGISTER FORM
# ════════════════════════════════════════════════════════

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'maxlength': '254',
        })
    )
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First name',
            'maxlength': '50',
        })
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last name',
            'maxlength': '50',
        })
    )

    class Meta:
        model  = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'e.g. rahul123  (letters + numbers required)',
            'minlength': '4',
            'maxlength': '30',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Create password (min 8 chars)',
            'minlength': '8',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password',
            'minlength': '8',
        })

    def clean_first_name(self):
        value = self.cleaned_data.get('first_name', '').strip()
        validate_name(value, 'First name')
        return value.title()

    def clean_last_name(self):
        value = self.cleaned_data.get('last_name', '').strip()
        validate_name(value, 'Last name')
        return value.title()

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        validate_username(username)
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError('This username is already taken. Please choose another.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if not email:
            raise ValidationError('Email address is required.')
        if len(email) > 254:
            raise ValidationError('Email address is too long.')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('An account with this email already exists.')
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1', '')
        validate_password_strength(password)
        return password


# ════════════════════════════════════════════════════════
# LOGIN FORM
# ════════════════════════════════════════════════════════

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username',
            'autofocus': True,
            'maxlength': '150',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password',
        })

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if not username:
            raise ValidationError('Username is required.')
        if len(username) > 150:
            raise ValidationError('Username is too long.')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password', '')
        if not password:
            raise ValidationError('Password is required.')
        return password


# ════════════════════════════════════════════════════════
# PRODUCT FORM
# ════════════════════════════════════════════════════════

class ProductForm(forms.ModelForm):
    class Meta:
        model  = Product
        fields = ['name', 'description', 'price', 'stock', 'category', 'image', 'is_available']
        widgets = {
            'name':         forms.TextInput(attrs={
                'class': 'form-control',
                'minlength': '2',
                'maxlength': '200',
                'placeholder': 'Product name (2–200 characters)',
            }),
            'description':  forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'maxlength': '1000',
                'placeholder': 'Product description (optional, max 1000 chars)',
            }),
            'price':        forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0.01',
                'max': '99999.99',
                'step': '0.01',
                'placeholder': 'e.g. 49.99',
            }),
            'stock':        forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '99999',
                'placeholder': 'e.g. 100',
            }),
            'category':     forms.Select(attrs={'class': 'form-select'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise ValidationError('Product name must be at least 2 characters.')
        if len(name) > 200:
            raise ValidationError('Product name cannot exceed 200 characters.')
        return name

    def clean_description(self):
        desc = self.cleaned_data.get('description', '').strip()
        if len(desc) > 1000:
            raise ValidationError('Description cannot exceed 1000 characters.')
        return desc

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None:
            raise ValidationError('Price is required.')
        if price <= 0:
            raise ValidationError('Price must be greater than zero.')
        if price > 99999.99:
            raise ValidationError('Price cannot exceed Rs.99,999.99.')
        return price

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock is None:
            raise ValidationError('Stock quantity is required.')
        if stock < 0:
            raise ValidationError('Stock cannot be negative.')
        if stock > 99999:
            raise ValidationError('Stock cannot exceed 99,999 units.')
        return stock

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and hasattr(image, 'size'):
            if image.size > 5 * 1024 * 1024:
                raise ValidationError('Image file size cannot exceed 5 MB.')
            allowed_types = ['image/jpeg', 'image/png', 'image/webp', 'image/gif']
            if hasattr(image, 'content_type') and image.content_type not in allowed_types:
                raise ValidationError('Only JPEG, PNG, WEBP, or GIF images are allowed.')
        return image

    def clean_category(self):
        category = self.cleaned_data.get('category', '').strip()
        valid_cats = [c[0] for c in Product.CATEGORY_CHOICES]
        if category not in valid_cats:
            raise ValidationError('Please select a valid category.')
        return category


# ════════════════════════════════════════════════════════
# CHECKOUT / DELIVERY ADDRESS FORM  (new)
# ════════════════════════════════════════════════════════

VALID_PAYMENT_METHODS = ['upi', 'card', 'cod', 'qr']


class CheckoutForm(forms.Form):
    payment_method = forms.ChoiceField(
        choices=[(m, m) for m in VALID_PAYMENT_METHODS],
        error_messages={'required': 'Please select a payment method.'},
    )
    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Full Name',
            'maxlength': '100',
            'id': 'id_full_name',
        }),
        error_messages={'required': 'Full name is required.'},
    )
    street_address = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Street Address, Area',
            'maxlength': '200',
            'id': 'id_street_address',
        }),
        error_messages={'required': 'Street address is required.'},
    )
    flat_no = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Flat / House No.',
            'maxlength': '50',
            'id': 'id_flat_no',
        }),
    )
    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'City',
            'maxlength': '100',
            'id': 'id_city',
        }),
        error_messages={'required': 'City is required.'},
    )
    state = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'State',
            'maxlength': '100',
            'id': 'id_state',
        }),
        error_messages={'required': 'State is required.'},
    )
    pin_code = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'PIN Code',
            'maxlength': '6',
            'pattern': r'\d{6}',
            'inputmode': 'numeric',
            'id': 'id_pin_code',
        }),
        error_messages={'required': 'PIN code is required.'},
    )
    phone = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone Number (10 digits)',
            'maxlength': '10',
            'inputmode': 'tel',
            'id': 'id_phone',
        }),
        error_messages={'required': 'Phone number is required.'},
    )

    def clean_full_name(self):
        name = self.cleaned_data.get('full_name', '').strip()
        validate_name(name, 'Full name')
        return name

    def clean_city(self):
        city = self.cleaned_data.get('city', '').strip()
        if not re.match(r"^[a-zA-Z\s\-']+$", city):
            raise ValidationError('City name can only contain letters and spaces.')
        return city.title()

    def clean_state(self):
        state = self.cleaned_data.get('state', '').strip()
        if not re.match(r"^[a-zA-Z\s\-']+$", state):
            raise ValidationError('State name can only contain letters and spaces.')
        return state.title()

    def clean_pin_code(self):
        pin = self.cleaned_data.get('pin_code', '').strip()
        if not re.match(r'^\d{6}$', pin):
            raise ValidationError('PIN code must be exactly 6 digits.')
        return pin

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        phone_digits = re.sub(r'[\s\-]', '', phone)
        if not re.match(r'^[6-9]\d{9}$', phone_digits):
            raise ValidationError(
                'Enter a valid 10-digit Indian mobile number starting with 6, 7, 8, or 9.'
            )
        return phone_digits

    def clean_payment_method(self):
        method = self.cleaned_data.get('payment_method', '').strip()
        if method not in VALID_PAYMENT_METHODS:
            raise ValidationError('Please select a valid payment method.')
        return method
