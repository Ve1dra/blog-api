from rest_framework import serializers
from users.models import Posts


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ["id", "owner", "heading", "content", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]
#
#
