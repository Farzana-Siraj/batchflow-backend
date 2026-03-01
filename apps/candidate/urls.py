from django.urls import path

from .views import CandidateCreateView, CandidateSearchView

urlpatterns = [
    path("create/", CandidateCreateView.as_view(), name="candidate-create"),
    path("search/", CandidateSearchView.as_view(), name="candidate-search"),
]
