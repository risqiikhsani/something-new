
# python manage.py admin_generator user

from django.contrib import admin

from .models import CustomUser, Profile, Connection, Request


from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError


from django.contrib.auth import get_user_model

from django.contrib.auth import get_user_model
User = get_user_model()

class UserCreationForm(forms.ModelForm):
	"""A form for creating new users. Includes all the required
	fields, plus a repeated password."""
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('username',)

	def clean_password2(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise ValidationError("Passwords don't match")
		return password2

	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super().save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user

class UserChangeForm(forms.ModelForm):
	"""A form for updating users. Includes all the fields on
	the user, but replaces the password field with admin's
	disabled password hash display field.
	"""
	password = ReadOnlyPasswordHashField(label=("Password"),
        help_text=("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"../password/\">this form</a>."))
	class Meta:
		model = User
		fields = ('email', 'password', 'phone_number', 'is_active', 'is_staff')
	
class UserAdmin(BaseUserAdmin):
	# The forms to add and change user instances
	form = UserChangeForm
	add_form = UserCreationForm

	# The fields to be used in displaying the User model.
	# These override the definitions on the base UserAdmin
	# that reference specific fields on auth.User.
	list_display = (
		'id',
		'last_login',
		'is_superuser',
		'username',
		'email',
		'is_staff',
		'is_active',
		'date_joined',
		'phone_number',
	)

	list_filter = (
		'last_login',
		'is_superuser',
		'is_staff',
		'is_active',
		'date_joined',
	)

	fieldsets = (
		(None, {'fields': ('username', 'password')}),
		('Personal info', {'fields': ('phone_number','email')}),
		('Permissions', {'fields': ('is_staff','is_active')}),
	)

	# add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
	# overrides get_fieldsets to use this attribute when creating a user.
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('username', 'password1', 'password2'),
		}),
	)

	search_fields = ('username',)

	ordering = ('username',)

	filter_horizontal = ()

admin.site.register(User,UserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = (
		'id',
		'user',
		'name',
		'public_username',
		'about',
		'profile_picture',
		'poster_picture',
	)
	list_filter = ('user',)
	search_fields = ('name',)





@admin.register(Connection)
class ConnectionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    list_filter = ('user',)
    raw_id_fields = ('connected',)

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'sender', 'time_creation')
    list_filter = ('user', 'sender', 'time_creation')