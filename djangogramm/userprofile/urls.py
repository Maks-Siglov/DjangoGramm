from django.urls import path

from userprofile import views

urlpatterns = [
    path("userprofile/<username>", views.profile, name="profile"),
    path(
        "userprofile/<username>/edit", views.edit_profile, name="edit_profile"
    ),
    path(
        "profile_registration/<str:link_key>/",
        views.profile_registration,
        name="profile_registration",
    ),
]