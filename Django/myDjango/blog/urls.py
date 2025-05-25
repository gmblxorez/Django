from django.urls import path
from . import views


app_name = "blog"
urlpatterns = [
    path("", views.index, name="index"),
    path("news", views.news, name="news"),
    path("contact", views.contact, name="contact"),
    path("detail/<int:pk>/", views.detail, name="blog_detail"),
    path("create/", views.create_blog, name="create_blog"),
    path("update/<int:pk>/", views.update_blog, name="update_blog"),
    path("delete/<int:pk>/", views.delete_blog, name="delete_blog"),
]
