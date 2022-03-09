from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from posts.models import Post, Group
from rest_framework import status, viewsets
from rest_framework.response import Response

from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.author:
            raise PermissionDenied()
        serializer.save(author=self.request.user, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionDenied()
        super().perform_destroy(instance)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.author:
            raise PermissionDenied()
        serializer.save(author=self.request.user,
                        status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionDenied()
        super().perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
