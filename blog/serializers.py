# nested serializer for detail, and author's blog_list
from rest_framework import serializers

from core.models import Blog, User


# todo: list & manage blogs ,
# todo: author filed auto assigned, can't edit
class BlogSerializer(serializers.ModelSerializer):
    """
    Serializer for blog management.
    author: fk
    """
    author = serializers.SlugRelatedField(slug_field='name',
                                          queryset=User.objects.all())

    class Meta:
        model = Blog
        fields = ('id', 'title', 'author', 'body', 'created', 'updated')
        read_only_fields = ('id',)
