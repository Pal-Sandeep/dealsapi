from django.urls import path

from deals.views import DealProjectAddCreateAPIView, DealViewSet, ProjectViewSet, index
from rest_framework import routers

router = routers.DefaultRouter()
router.register('projects', ProjectViewSet, basename='projects')
router.register('deals', DealViewSet, basename='deals')


urlpatterns = [
    # editing existing deals with projects
    path('', index, name='index'),

    path("deals/<int:pk>/project/add",
         DealProjectAddCreateAPIView.as_view()),
] + router.urls
