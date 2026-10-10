from rest_framework.throttling import UserRateThrottle
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_headers
from django.core.cache import cache

from users.serializers import PostSerializer
from drf_yasg import openapi
from django.db.models import Q
from drf_yasg.utils   import swagger_auto_schema
from django.shortcuts import get_object_or_404, get_list_or_404
from utils.paginations import CustomPagination
from users.models import Posts

 # Create your views here.

class PostView(generics.GenericAPIView):
    serializer_class = PostSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        posts = get_list_or_404(Posts.objects.all())
        return posts
    # @method_decorator(cache_page(60 * 2))
    def get(self, request, format=None):
        key = f"all_posts:{request.user.id}"
        cached = cache.get(key)
        if cached:
            print("Cached HIT")
            return Response(cached, status=200)

        all_posts = self.get_queryset()
        pagination = self.paginate_queryset(all_posts)
        if pagination is not None:
            serializer = self.serializer_class(all_posts, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(all_posts, many=True)
        print("Getting from the DB")
        cache.set(key, serializer.data, 120)
        return Response(serializer.data, status=200)

    def post(self, request):
        key = f"all_posts:{request.user.id}"
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        cache.delete(key)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

class PostsCRUD(generics.GenericAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        id = self.kwargs["id"]
        posts = get_object_or_404(Posts, id=id)
        return posts

    def patch(self, request, id, format=None):
        key = f"all_posts:{request.user.id}"
        all_posts = self.get_queryset()
        serializer = self.serializer_class(data=request.data, instance=all_posts, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cache.delete(key)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        key = f"all_posts:{request.user.id}"
        post = self.get_queryset()
        post.delete()
        cache.delete(key)
        return Response(status=200)

class PostSearch(generics.GenericAPIView):
    serializer_class = PostSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        search = self.request.query_params.get("search", None)
        all_posts = Posts.objects.all()
        if search:
            all_posts = all_posts.filter(Q(heading__icontains=search) | Q(content__icontains=search))
        return all_posts

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "search", openapi.IN_QUERY,
                description="Looking for something?",
                required=False, type=openapi.TYPE_STRING)
        ]
    )

    def get(self, request, format=None):
        key = f"all_posts:{request.user.id}"
        cached = cache.get(key)
        if cached is not None:
            print("Cached HIT")
            return Response(cached, status=200)

        all_posts = self.get_queryset()
        pagination = self.paginate_queryset(all_posts)
        if pagination is not None:
            serializer = self.serializer_class(all_posts, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(all_posts, many=True)
        print("Fetching from the DB")
        cache.set(key, serializer.data, 120)
        return Response(data=serializer.data, status=status.HTTP_200_OK)