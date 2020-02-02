from django.urls import path, include
from rest_framework.routers import DefaultRouter

from blog import views

router = DefaultRouter()
router.register('all', views.ReadOnlyBlogViewSet, 'all')
router.register('mine', views.ManageBlogViewSet, 'mine')

app_name = 'blog'

urlpatterns = [
    path('', include(router.urls)),
]
