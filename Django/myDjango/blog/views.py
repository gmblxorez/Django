from datetime import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .forms import BlogModelForm, CommentModelForm
from .models import Blog, Comment


def index(request):

    latest_blogs = Blog.objects.order_by('-date_published')[:3]

    context = {
        'latest_blogs': latest_blogs,
        'title': 'Главная страница',
    }
    return render(request, 'blog/index.html', context)


def news(request):
    blogs = Blog.objects.all()
    search = request.GET.get("search")

    if search:
        blogs = blogs.filter(title__icontains=search)

    paginator = Paginator(blogs, per_page=3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    title = "Новости"
    return render(request, template_name='blog/blog_list.html', context={"page_obj": page_obj, "title": title})


def contact(request):
    title = "Контакты"

    context = {
        'title':  title,
        'company_name': 'Ведьмачие новости',
        'address': 'Г.Мосвка, Ул.Ведьмачья, д35',
        'phone_number': '+795545313',
        'email': 'vgromyko64@gmail.com',
    }
    return render(request, 'blog/contact.html', context)


def detail(request, pk):
    blogs = Blog.objects.all()
    blog = blogs.get(pk=pk)
    title = blog.title

    count = str(request.GET.get("post"))
    comments = Comment.objects.filter(blog=blog).order_by("-date_published")

    if count == "prev":
        if blog.id == blogs.first().id:
            return redirect("blog:blog_detail", pk=blogs.last().id)
        prev_blog = blogs.filter(id__lt=blog.id).last()
        return redirect("blog:blog_detail", pk=prev_blog.id)

    if count == "next":
        if blog.id == blogs.last().id:
            return redirect("blog:blog_detail", pk=blogs.first().id)
        next_blog = blogs.filter(id__gt=blog.id).first()
        return redirect("blog:blog_detail", pk=next_blog.id)
    centext = {
        "blog": blog,
        "title": title,
        "comments": comments
    }

    if request.method == "POST":
        form = CommentModelForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.date_published = datetime.now()
            new_comment.blog = blog
            new_comment.save()
            return redirect("blog:blog_detail", pk=pk)

    else:
        form = CommentModelForm
    centext["form"] = form
    return render(request, template_name='blog/blog_detail.html', context=centext)


@permission_required("blog.add_blog")
@login_required
def create_blog(request):
    title = "Создание новости"
    action = "Создать"
    if request.method == "POST":
        form = BlogModelForm(request.POST, request.FILES)
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.author = request.user
            new_blog.date_published = datetime.now()
            new_blog.save()
            return redirect("blog:index")
    else:
        form = BlogModelForm()
    return render(request, template_name='blog/create_update_blog.html', context={"title": title, "form": form, "action": action})


def is_owner(func):

    def wrapper(request, *args, **kwargs):
        blog_id = kwargs["pk"]
        if blog_id:
            blog = Blog.objects.get(pk=blog_id)
            if blog.author == request.user or request.user.is_superuser:
                return func(request, *args, **kwargs)
        return redirect("blog:index")
    return wrapper


@is_owner
@login_required
def update_blog(request, pk):
    action = "Обновить"
    blog = Blog.objects.get(pk=pk)
    title = f"Редактирование { blog.title }"
    if request.method == "POST":
        form = BlogModelForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect("blog:blog_detail", pk=pk)
    else:
        form = BlogModelForm(instance=blog)
    return render(request, template_name='blog/create_update_blog.html', context={"title": title, "form": form, "action": action})


@is_owner
@login_required
def delete_blog(request, pk):
    blog = Blog.objects.get(pk=pk)
    blog.delete()
    return redirect("blog:index")


