from django.urls import path, include
from rest_framework import routers, serializers, viewsets

from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/guides/', views.get_guides, name="get_guides"),
    path('v1/guides/<int:pk>/', views.get_guide, name="get_guide"),
    path('v1/guides/create/', views.create_guide, name="create_guide"),
    path('v1/guides/update/<int:pk>/', views.update_guide, name="update_guide"),
    path('v1/guides/create_availability/', views.create_guide_availability,
         name="create_guide_availability"),
    path('v1/guides/<int:pk>/availability_between_dates/', views.get_guide_availability_between_dates,
         name="availability_between_dates"),
    path('v1/guides/<int:pk>/availability_by_day/', views.get_guide_availability_by_day,
         name="get_guide_availability_by_day"),
    path('v1/guides/<int:pk>/availability/', views.get_guide_availability,
         name="get_guide_availability"),
    path('v1/destinations/', views.get_destinations, name="get_destinations"),
    path('v1/tours/', views.get_tours, name="get_tours"),
]
