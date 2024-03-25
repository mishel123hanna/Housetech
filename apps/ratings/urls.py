from django.urls import path

from . import views

urlpatterns = [
    path("<str:profile_id>/", views.add_agent_review, name="add-rating")
]
