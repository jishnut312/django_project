from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse
from user_auth.models import UserProfile
from accounts.models import Post
from django.core.exceptions import ValidationError

from accounts.views import *

# User Registration View
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from .models import UserProfile, LoginTable

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.csrf import csrf_protect
from django.core.validators import validate_email
from django.core.files.images import get_image_dimensions
import re
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.csrf import csrf_protect
from django.core.validators import validate_email
import re
from django.db import IntegrityError

# views.py
from django.contrib.auth.models import User
from .models import UserProfile
from django.shortcuts import render, redirect
from django.contrib import messages

def userRegistration(request):
    if request.method == 'POST':
        try:
            # Get form data
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            contact_number = request.POST.get('contact_number')
            profile_pic = request.FILES.get('profile_pic')

            # Validate required fields
            if not all([username, email, password, password2, first_name, last_name]):
                raise ValidationError("All fields are required except profile picture and contact number")

            # Check if passwords match
            if password != password2:
                raise ValidationError("Passwords do not match")

            # Validate email format
            if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
                raise ValidationError("Invalid email format")

            # Validate contact number format if provided
            if contact_number and not re.match(r'^\+?1?\d{9,15}$', contact_number):
                raise ValidationError("Phone number must be in the format: '+999999999'")

            # Check if username exists
            if User.objects.filter(username=username).exists():
                raise ValidationError("Username already exists. Please choose a different one.")

            # Check if email exists
            if User.objects.filter(email=email).exists():
                raise ValidationError("Email already registered. Please use a different email.")

            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Create profile
            profile = UserProfile.objects.create(
                user=user,
                contact_number=contact_number
            )

            # Handle profile picture
            if profile_pic:
                profile.profile_pic = profile_pic
                profile.save()

            messages.success(request, "Registration successful! Please log in.")
            return redirect('userLogin')

        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f"An error occurred during registration: {str(e)}")

    return render(request, 'register.html')
@csrf_protect
def userLogin(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('adminview')
        return redirect('feed')

    next_url = request.GET.get('next', '')
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = ''

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            messages.error(request, 'Both username and password are required')
            return render(request, 'login.html', {'next': next_url})

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            # Safe redirect
            if next_url:
                return redirect(next_url)
            
            # Role-based redirect
            if user.is_superuser:
                return redirect('adminview')
            return redirect('feed')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html', {'next': next_url})

def userLogout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('userLogin')
# Forgot Password View
def forgot_password(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        # Check if passwords match
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('forgot_password')

        # Hash the new password
        hashed_password = make_password(new_password)

        try:
            # Fetch the user from userprofile and logintable
            user = UserProfile.objects.get(username=username,  user__email=email)
            login_entry = LoginTable.objects.get(username=username)

            # Update both tables with the new hashed password
            user.password = hashed_password
            login_entry.password = hashed_password

            # Save the changes
            user.save()
            login_entry.save()

            messages.success(request, "Password reset successful. Please log in.")
            return redirect('userLogin')

        except UserProfile.DoesNotExist:
            messages.error(request, "User not found with that username and email")
            return redirect('forgot_password')

    return render(request, 'forgot_password.html')


# User Logout View



from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User

def is_superuser(user):
    return user.is_superuser



@login_required
@user_passes_test(lambda u: u.is_superuser)
def adminview(request):
    users = User.objects.all().select_related('userprofile')
    posts = Post.objects.all()
    return render(request, 'adminview.html', {
        'users': users,
        'posts': posts
    })

# Apply the same decorator to all admin views
@login_required
@user_passes_test(lambda u: u.is_superuser)
def view_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'ad/view_user.html', {'user': user})
@login_required
@user_passes_test(lambda u: u.is_superuser)
def block_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = user.userprofile
    profile.blocked = True
    profile.save()
    messages.success(request, f"User {user.username} has been blocked")
    return redirect('adminview')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def unblock_user(request, user_id):
    """
    Unblocks a user - only accessible by superusers
    """
    # Get the user to unblock
    user = get_object_or_404(User, id=user_id)
    
    # Check if user has a profile
    if not hasattr(user, 'userprofile'):
        messages.error(request, "User profile not found")
        return redirect('adminview')
    
    # Unblock the user
    user.userprofile.blocked = False
    user.userprofile.save()
    
    messages.success(request, f"User {user.username} has been unblocked successfully")
    return redirect('adminview')
@login_required
@user_passes_test(is_superuser)
def unblock_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.blocked = False
    post.save()
    messages.success(request, f"Post '{post.title}' has been unblocked")
    return redirect('adminview')

@login_required
@user_passes_test(is_superuser)
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post_title = post.title
    post.delete()
    messages.success(request, f"Post '{post_title}' has been deleted")
    return redirect('adminview')

@login_required
@user_passes_test(is_superuser)
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.is_superuser and user != request.user:
        messages.error(request, "Cannot edit other superusers")
        return redirect('adminview')
        
    # Your logic to edit the user goes here
    return render(request, 'ad/edit_user.html', {'user': user})

@login_required
@user_passes_test(is_superuser)
def view_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'ad/view_post.html', {'post': post})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    """
    Deletes a user account - only accessible by superusers
    Prevents deletion of other superusers and self-deletion
    """
    # Get the user to delete
    user_to_delete = get_object_or_404(User, id=user_id)
    
    # Prevent deleting yourself
    if user_to_delete == request.user:
        messages.error(request, "You cannot delete your own account!")
        return redirect('adminview')
    
    # Prevent deleting other superusers
    if user_to_delete.is_superuser:
        messages.error(request, "Cannot delete other superuser accounts!")
        return redirect('adminview')
    
    # Delete the user
    username = user_to_delete.username
    user_to_delete.delete()
    
    messages.success(request, f"User '{username}' has been permanently deleted")
    return redirect('adminview')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def block_post(request, post_id):
    """
    Blocks a post - only accessible by superusers
    Prevents blocking of posts that are already blocked
    """
    # Get the post to block
    post = get_object_or_404(Post, id=post_id)
    
    # Check if post is already blocked
    if post.blocked:
        messages.warning(request, f"Post '{post.title}' is already blocked")
        return redirect('adminview')
    
    # Block the post
    post.blocked = True
    post.save()
    
    messages.success(request, f"Post '{post.title}' has been blocked")
    return redirect('adminview')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def ad_delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        post_title = post.title
        post.delete()
        messages.success(request, f"Post '{post_title}' has been deleted successfully.")
        return redirect('adminview')  # Make sure 'adminview' is the correct URL name
        
    # If not a POST request, show a confirmation page
    context = {
        'post': post,
        'title': 'Confirm Post Deletion'
    }
    return render(request, 'ad/confirm_post_delete.html', context)