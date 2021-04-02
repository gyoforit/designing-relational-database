from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST, require_safe, require_http_methods
from .forms import ReviewForm, CommentForm
from .models import Review, Comment
from django.core.paginator import Paginator
from datetime import datetime, timedelta

User = get_user_model()

# Create your views here.
@require_safe
def index(request):
    reviews_all = Review.objects.order_by('-pk')
    page = int(request.GET.get('p', 1))
    paginator = Paginator(reviews_all, 10)
    reviews = paginator.get_page(page)
    current = datetime.today()
    ten_minutes_before = current - timedelta(minutes=10)
    new_reviews = Review.objects.filter(created_at__date=current, created_at__time__gt=ten_minutes_before.time())
    context = {
        'reviews': reviews,
        'ten_minutes_before': ten_minutes_before,
        'new_reviews': new_reviews,
    }
    return render(request, 'community/index.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('community:index')
    else:
        form = ReviewForm()
    context = {
        'form': form,
    }
    return render(request, 'community/form.html', context)


@require_safe
def detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comment_form = CommentForm()
    comments = review.comment_set.all()
    context = {
        'review': review,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'community/detail.html', context)



def delete(request, review_pk):
    if request.method == 'POST' and request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        if request.user == review.user:
            review.delete()
    return redirect('community:index')


@login_required
@require_http_methods(['GET', 'POST'])
def update(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user == review.user:
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                return redirect('community:detail', review.pk)
        else:
            form = ReviewForm(instance=review)
        context = {
            'form': form,
        }
        return render(request, 'community/form.html', context)
    return redirect('community:detail', review.pk)


@login_required
def comments_create(request, review_pk):
    if request.method == 'POST':
        review = get_object_or_404(Review, pk=review_pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.review = review
            comment.user = request.user
            comment.save()
            return redirect('community:detail', review.pk)
        context = {
            'comment_form': comment_form,
            'review': review,
        }
        return render(request, 'community/detail.html', context)
    return redirect('community:detail', review.pk)


def comment_delete(request, review_pk, comment_pk):
    if request.method == 'POST' and request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
        return redirect('community:detail', review_pk)
    return redirect('community:index')
    

@require_POST
def like(request, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        if review.like_users.filter(pk=request.user.pk).exists():
            review.like_users.remove(request.user)
        else:
            review.like_users.add(request.user)
        return redirect('community:detail', review.pk)
    return redirect('accounts:login')