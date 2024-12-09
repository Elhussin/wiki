from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entery>", views.enterys, name="wiki"),
    path("serarch", views.serarchs, name="serarch"),
    path("new", views.new_pages, name="new"),
    path("edit/<str:entery>", views.edit_pages, name="edit"),
    path("randomq", views.randomq, name="randomq")
]
