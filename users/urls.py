from django.urls import path

from users.views import PostView, PostsCRUD, PostSearch

urlpatterns = [
    path('posts/', PostView.as_view()),
    path('patch/<uuid:id>/', PostsCRUD.as_view()),
    path('look/', PostSearch.as_view()),
]