from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from blog.serializers import BlogSerializer
from core.models import Blog


class RetrieveListBlogViewSet(viewsets.ReadOnlyModelViewSet):
    """Retrieve & List Blog"""
    queryset = Blog.objects.all().order_by('-updated')
    serializer_class = BlogSerializer

#
# class ManageBlogViewSet(viewsets.ModelViewSet):
#     """Manage blog api for author"""
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     serializer_class = BlogSerializer
#
