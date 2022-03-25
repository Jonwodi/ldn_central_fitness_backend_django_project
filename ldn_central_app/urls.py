from django.urls import path

from . import views

urlpatterns = [
    path("gyms/", views.GymListCreateView.as_view(), name="gym-list-create"),
    path(
        "gyms/<str:pk>",
        views.GymRetrieveUpdateDestroyView.as_view(),
        name="gym-retrieve-update-destroy",
    ),
    path(
        "registrations/",
        views.RegistrationCreateView.as_view(),
        name="registration-create",
    ),
    path("sessions/", views.SessionCreateView.as_view(), name="session-create"),
    path(
        "session/",
        views.SessionRetrieveDestroyView.as_view(),
        name="session-retrieve-destroy",
    ),
]
