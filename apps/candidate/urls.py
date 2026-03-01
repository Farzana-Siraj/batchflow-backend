from django.urls import path

from .views import CandidateCreateView

urlpatterns = [
    path("create/", CandidateCreateView.as_view(), name="candidate-create"),
]
