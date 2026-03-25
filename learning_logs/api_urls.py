from django.urls import path
from . import api_views

app_name = "api"

urlpatterns = [
    path("topics/", api_views.TopicListCreateAPIView.as_view(), name="topics"),
    path("topics/<int:pk>/", api_views.TopicDetailAPIView.as_view(), name="topic-detail"),
    path("entries/", api_views.EntryListCreateAPIView.as_view(), name="entries"),
    path("entries/<int:pk>/", api_views.EntryDetailAPIView.as_view(), name="entry-detail"),
]