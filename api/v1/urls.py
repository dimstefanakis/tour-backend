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
    path('v1/guides/<int:pk>/create_availability/', views.create_guide_availability,
         name="create_guide_availability"),
    path('v1/guides/<int:pk>/create_availability_multiple_dates/', views.create_guide_availability_multiple_dates,
         name="create_availability_multiple_dates"),
    path('v1/guides/<int:pk>/availability_between_dates/', views.get_guide_availability_between_dates,
         name="availability_between_dates"),
    path('v1/guides/<int:pk>/availability_by_day/', views.get_guide_availability_by_day,
         name="get_guide_availability_by_day"),
    path('v1/guides/<int:pk>/availability/', views.get_guide_availability,
         name="get_guide_availability"),
    path('v1/guides/availability_by_day/',
         views.get_available_guides_by_day, name="get_available_guides_by_day"),
    path('v1/guides/<int:pk>/data_per_month/', views.get_guides_with_tours_by_month,
         name="data_per_month"),
    path('v1/destinations/', views.get_destinations, name="get_destinations"),
    path('v1/tours/', views.get_tours, name="get_tours"),
    path('v1/tours/create/', views.create_tour, name="create_tour"),
    path('v1/tours_by_destination/<int:pk>/',
         views.get_tours_by_destination, name="get_tours_by_destination"),
    path('v1/tours_by_destination_and_day/<int:pk>/',
         views.get_tours_by_destination_and_day, name="get_tours_by_destination_and_day"),
    path('v1/locations/', views.get_locations, name="get_locations"),
    path('v1/assign_guide_to_tour/<int:pk>/',
         views.assign_guide_to_tour, name="assign_guide_to_tour"),
]
