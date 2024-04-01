from django.urls import path

from .views import (
            CratesListCreateAPIView, 
            CrateDetailView,
            GenerateCrateShareLink
        )

urlpatterns = [
    path('crates_list/', CratesListCreateAPIView.as_view()),
    path('crate_detail/<slug>/<school_id>', CrateDetailView.as_view(), name="crate-detail"),

    path('share-crate/<slug>', GenerateCrateShareLink.as_view())
]