# nested serializer for detail, and author's blog_list
from rest_framework import serializers, generics, mixins

from core.models import Blog


class BlogSerializer(serializers.ModelSerializer):
    """
    Serializer for blog objects.
    author: fk
    """

    author = serializers.SerializerMethodField()

    def get_author(self, blog):
        return blog.author.name

    class Meta:
        model = Blog
        fields = ['id', 'title', 'body', 'created', 'updated', 'author']
