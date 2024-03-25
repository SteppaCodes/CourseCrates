from django.urls import path
from .views import (CreateSchool, SchoolsListView)

urlpatterns = [
    path('create-school/<name>/<abv>/', CreateSchool.as_view(), name='create_school'),
    path('schools-list/', SchoolsListView.as_view(), name='school_list'),

]
