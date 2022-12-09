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
]
