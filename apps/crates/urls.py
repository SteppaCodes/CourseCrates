from django.urls import path

from .views import CratesListCreateView, CrateDetailView

urlpatterns = [
    path('crates_list/', CratesListCreateView.as_view()),
    path('crate_detail/<uuid:id>/', CrateDetailView.as_view())
]