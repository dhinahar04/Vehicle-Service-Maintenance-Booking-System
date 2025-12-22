from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import User, Vehicle, ServiceCenter, Mechanic, Booking, ServiceCategory, Feedback, Inventory


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Bootstrap classes and placeholders to widgets
        for name, field in self.fields.items():
            # Use form-select for select widgets
            if isinstance(field.widget, (forms.Select, forms.NullBooleanSelect)):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                # Default to form-control for text/password inputs
                field.widget.attrs.update({'class': 'form-control'})

        # Friendly placeholders
        placeholders = {
            'username': 'Username',
            'email': 'Email',
            'first_name': 'First name',
            'last_name': 'Last name',
            'phone': 'Phone',
            'password1': 'Password',
            'password2': 'Confirm password',
        }
        for fname, ph in placeholders.items():
            if fname in self.fields:
                self.fields[fname].widget.attrs.update({'placeholder': ph})

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'role', 'password1', 'password2')

class MechanicCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    specialization = forms.CharField(max_length=200, required=False)
    experience_years = forms.IntegerField(required=False, min_value=0)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply bootstrap classes
        for name, field in self.fields.items():
            if isinstance(field.widget, (forms.Select, forms.NullBooleanSelect)):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

        # placeholders
        if 'username' in self.fields:
            self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        if 'email' in self.fields:
            self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm password'})
        if 'specialization' in self.fields:
            self.fields['specialization'].widget.attrs.update({'placeholder': 'e.g., Engine Repair'})
        if 'experience_years' in self.fields:
            self.fields['experience_years'].widget.attrs.update({'placeholder': '0'})

    def save(self, service_center, commit=True):
        # Create the user first
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email', '')
        user.role = 'mechanic'
        if commit:
            user.save()
            Mechanic.objects.create(
                user=user,
                service_center=service_center,
                specialization=self.cleaned_data.get('specialization', ''),
                experience_years=self.cleaned_data.get('experience_years') or 0
            )
        return user


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_type', 'brand', 'model', 'year', 'registration_number', 'color', 'mileage']
        widgets = {
            'vehicle_type': forms.Select(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'registration_number': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'mileage': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class ServiceCenterForm(forms.ModelForm):
    class Meta:
        model = ServiceCenter
        fields = ['name', 'description', 'address', 'phone', 'email', 'opening_time', 'closing_time']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'opening_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'closing_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['vehicle', 'service_center', 'service_category', 'booking_date', 'booking_time', 'service_description']
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-control'}),
            'service_center': forms.Select(attrs={'class': 'form-control'}),
            'service_category': forms.Select(attrs={'class': 'form-control'}),
            'booking_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'booking_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'service_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['item_name', 'description', 'quantity', 'unit_price', 'reorder_level']
        widgets = {
            'item_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'reorder_level': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Current Password'
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='New Password'
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Confirm New Password'
    )



