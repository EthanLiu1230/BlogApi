from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from blog.serializers import BlogSerializer
from core.models import Blog


class ReadOnlyBlogViewSet(viewsets.ReadOnlyModelViewSet):
    """Retrieve & List all blogs"""
    queryset = Blog.objects.all().order_by('-updated')
    serializer_class = BlogSerializer


class ManageBlogViewSet(viewsets.ModelViewSet):
    """
    crud blog api by specific user.
    """
    # ModelViewSet:
    # you'll normally need to provide at least the
    # 'queryset' and 'serializer_class' attributes.
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = BlogSerializer

    def get_queryset(self):
        queryset = Blog.objects.all()
        queryset = queryset.filter(author=self.request.user)
        return queryset

    def perform_create(self, serializer):
        """
        Create a new recipe.
        save current user to author
        """
        serializer.save(author=self.request.user)
