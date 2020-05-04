from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('movies', views.MovieViewSet, 'movies')
router.register('feedback', views.UserFeedbackViewSet, 'feedback')

urlpatterns = [
]
urlpatterns = urlpatterns + router.urls