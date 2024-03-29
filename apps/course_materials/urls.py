from django.urls import path 

from .views import MaterialsListCreateAPIView, CreateCourseAPIView


urlpatterns = [
    path('course-materials/', MaterialsListCreateAPIView.as_view(), name='create-material'),
    path('create-course/<code>/<title>', CreateCourseAPIView.as_view(), name='create-course')
]
