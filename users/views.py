from rest_framework.throttling import UserRateThrottle
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_cookie, vary_on_headers

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
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        posts = get_list_or_404(Posts.objects.all())
        return posts

    @method_decorator(cache_page(60 * 10))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request, format=None):
        all_posts = self.get_queryset()
        serializer = self.serializer_class(all_posts, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
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
        all_posts = self.get_queryset()
        serializer = self.serializer_class(data=request.data, instance=all_posts, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        post = self.get_queryset()
        post.delete()
        post.save()
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
    @method_decorator(cache_page(60 * 10))
    @method_decorator(vary_on_headers("Authentication"))
    def get(self, request, format=None):
        all_posts = self.get_queryset()
        serializer = self.serializer_class(all_posts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)