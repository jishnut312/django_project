from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Post, Comment
from django.db.models import Q
from django.core.paginator import Paginator
from .forms import PostForm, CommentForm,ProfileForm  # Import the necessary forms

# Feed View (Shows posts with search and pagination)
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Post

def feed(request):
    # Get base queryset (only non-blocked posts)
    posts = Post.objects.filter(blocked=False)
    
    # Search functionality
    query = request.GET.get('q', '')
    if query:
        posts = posts.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        )
    
    # Order and paginate
    posts = posts.order_by('-created_at')
    paginator = Paginator(posts, 6)  # 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/feed.html', {
        'posts': page_obj.object_list,  # Actual posts for current page
        'page_obj': page_obj,           # Pagination object
        'query': query                  # Search query
    })

# Create Post View (For authenticated users to create a new post)
from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Post

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # assuming user must be logged in
            post.save()
            return redirect('feed')  # adjust to your actual feed view name
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})


# Post Detail View (Shows individual post details and related comments)
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comment_form = CommentForm()

    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                redirect('post_detail', post_id=post.id)  


    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comment_form': comment_form,
    })
# Like Post View (To like or unlike a post)
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post,  id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        messages.info(request, "You unliked the post.")
    else:
        post.likes.add(request.user)
        messages.success(request, "You liked the post.")

    return redirect(request.META.get('HTTP_REFERER', 'feed'))

# Delete Post View (For post authors to delete their post)
@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user == post.author:
        post.delete()
        messages.success(request, "Post deleted successfully.")
    else:
        messages.error(request, "You can only delete your own posts.")

    return redirect('feed')


from .forms import CommentForm  # Make sure this is imported

@login_required
def edit_comment(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk, post__pk=post_pk)

    if request.user != comment.author:
        messages.error(request, "You can only edit your own comments.")
        return redirect('post_detail', post_id=post_pk)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Your comment has been updated!")
            return redirect('post_detail', post_id=post_pk)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'blog/edit_comment.html', {'form': form, 'comment': comment})


# Delete Comment View (For users to delete their own comments)
@login_required
def delete_comment(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk, post__pk=post_pk)

    if request.user == comment.author:
        comment.delete()
        messages.success(request, "Your comment has been deleted.")
    else:
        messages.error(request, "You can only delete your own comments.")

    return redirect('post_detail', post_id=post_pk)

# Profile View (User profile page where they can view/edit their profile)
@login_required
def profile(request):
    # User can edit their profile
    user_profile = request.user.userprofile  # Correct access to profile

    if request.method == 'POST':
        user_profile = request.user.profile
        user_profile.firstname = request.POST.get('firstname')
        user_profile.lastname = request.POST.get('lastname')
        user_profile.email = request.POST.get('email')
        user_profile.contact_number = request.POST.get('contactnumber')
        profilepic = request.FILES.get('profile_pic')
        if profilepic:
            user_profile.profilepic = profilepic
        user_profile.user.save()  # Save User model fields

        user_profile.save()
        messages.success(request, "Profile updated successfully!")

    return render(request, 'blog/profile.html', {'user': request.user})
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post,id=post_id)

    # Ensure that only the author can edit the post
    if post.author != request.user:
        messages.error(request, "You can only edit your own posts.")
        return redirect('post_detail', post_id=post.id)

    if request.method == 'POST':
        # Get the updated data from the form
        title = request.POST['title']
        content = request.POST['content']
        image = request.FILES.get('image', post.image)  # Keep the existing image if no new one is uploaded

        # Update the post
        post.title = title
        post.content = content
        post.image = image
        post.save()

        messages.success(request, "Your post has been updated successfully!")
        return redirect('post_detail',post_id=post_id)

    return render(request, 'blog/edit_post.html', {'post': post})

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import os

@login_required
def edit_profile(request):
    if request.method == 'POST':
        # Get the user's profile
        profile = request.user.userprofile
        
        # Handle file upload
        if 'profile_pic' in request.FILES:
            # Delete old file if it exists
            if profile.profile_pic:
                if os.path.isfile(profile.profile_pic.path):
                    os.remove(profile.profile_pic.path)
            # Save new file
            profile.profile_pic = request.FILES['profile_pic']
        
        # Update other fields
        profile.bio = request.POST.get('bio', '')
        profile.birth_date = request.POST.get('birth_date')
        profile.contactnumber = request.POST.get('contactnumber')
        
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return render(request, 'blog/edit_profile.html')