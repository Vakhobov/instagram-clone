from django.core.serializers import serialize
from django.shortcuts import render
from django.template.backends.django import reraise
from django.template.defaulttags import comment
from docs.conf import author
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import  Post, PostLike, PostComment, CommentLike
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from .serializer import PostSerializer, PostLikeSerializer, CommentLikeSerializer, CommentSerializer
from shared.custom_pagination import CustomPagination


class PostListApiView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny, ]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Post.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}
class PostCreateView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, ]

    def put(self, request, *args, **kwargs):
        post = self.get_object()
        serializer = self.serializer_class(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "success":True,
                "code": status.HTTP_200_OK,
                "message":"Post successfully updated",
                "data":serializer.data
            }
        )
    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        post.delete()
        return Response(
            {
                "success":True,
                "code":status.HTTP_204_NO_CONTENT,
                "message":"Post successfully deleted",
            }
        )

class PostCommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        post_id = self.kwargs['pk']
        queryset = PostComment.objects.filter(post_id=post_id)
        return queryset

class PostCommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        post_id = self.kwargs['pk']
        serializer.save(author=self.request.user, post_id=post_id)
        return serializer



class CommentListCreateApiView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    queryset = PostComment.objects.all()
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostLikeListView(generics.ListCreateAPIView):
    serializer_class = PostLikeSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        post_id = self.kwargs['pk']
        return PostLike.objects.filter(post_id=post_id)

class CommentRetrieveView(generics.RetrieveAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny, ]
    queryset = PostComment.objects.all()


class CommentLikeListView(generics.ListAPIView):

    serializer_class = CommentLikeSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        comment_id = self.kwargs['pk']
        return CommentLike.objects.filter(comment_id=comment_id)

class CommentsLikes(generics.ListAPIView):
    serializer_class =CommentLikeSerializer
    permission_classes = [AllowAny, ]
    queryset = CommentLike.objects.all()

class CommentLikeCreateView(generics.CreateAPIView):
    serializer_class = CommentLikeSerializer
    permission_classes = [AllowAny, ]
    queryset = CommentLike.objects.all()
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class PostLikeApiView(APIView):

    def post(self, request, pk):
        try:
            post_like = PostLike.objects.get(
                author=self.request.user,
                post_id=pk
            )
            post_like.delete()
            data = {
                "success": True,
                "message": "Like muaffaqiyatli o'chirildi"
            }
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        except PostLike.DoesNotExist:
            post_like = PostLike.objects.create(
                author=self.request.user,
                post_id=pk
            )
            serializer = PostLikeSerializer(post_like)
            data = {
                    "success":True,
                    "message":"Postga layk muaffaqiyatli qo'shildi",
                    "data": serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)










    #         post_like = PostLike.objects.create(
    #             author=self.request.user, post_id=pk
    #         )
    #         serializer = PostLikeSerializer(post_like)
    #         data = {
    #             "success":True,
    #             "message":"Postga layk muaffaqiyatli qo'shildi",
    #             "data": serializer.data
    #         }
    #         return Response(data, status=status.HTTP_201_CREATED)
    #     except Exception as e:
    #         data = {
    #             "success": False,
    #             "message": f"{str(e)}",
    #             "data": None
    #         }
    #         return Response(data, status=status.HTTP_400_BAD_REQUEST)
    #
    # # def delete(self, request, pk):
    #     try:
    #         post_like = PostLike.objects.get(author=self.request.user, post_id=pk)
    #         post_like.delete()
    #         data = {
    #             "success":True,
    #             "message":"Like postdan muaffaqiyatli o'chirildi",
    #             "data": None
    #         }
    #         return Response(
    #             data, status=status.HTTP_200_OK
    #         )
    #     except Exception as e:
    #         data = {
    #             "success": False,
    #             "message": f"{str(e)}",
    #             "data": None
    #         }
    #         return Response(data, status=status.HTTP_400_BAD_REQUEST)


class CommentLikeApiView(APIView):
    def post(self, request, pk):
        try:
            comment_like = CommentsLikes.objects.get(
                author=self.request.user,
                comment_id=pk
            )
            comment_like.delete()
            data = {
                "success": True,
                "message": "Kommentdan Like muaffaqiyatli o'chirildi"
            }
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        except CommentLike.DoesNotExist:
            comment_like = CommentsLikes.objects.create(
                author=self.request.user,
                comment_id=pk
            )
            serializer = CommentLikeSerializer(comment_like)

            data = {
                "success": True,
                "message": "Kommentga Like muaffaqiyatli qo'shildi",
                "data": serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)





    #         comment_like = CommentLike.objects.create(author=self.request.user, comment_id=pk)
    #         serializer = CommentLikeSerializer(comment_like)
    #         data = {
    #             "success":True,
    #             "message": "Kommentga muaffaqiyatli like bosildi",
    #             "data": serializer.data
    #         }
    #         return Response(data, status=status.HTTP_201_CREATED)
    #     except Exception as e:
    #         data = {
    #             "success":False,
    #             "message":f"{str(e)}",
    #             "data":None
    #         }
    #         return Response (data, status=status.HTTP_400_BAD_REQUEST)
    # def delete(self, request, pk):
    #     try:
    #         comment_like = CommentLike.objects.get(
    #             author=self.request.user,
    #             comment_id=pk
    #         )
    #         comment_like.delete()
    #         data = {
    #             "success":True,
    #             "message":"Like muaffaqiyatli o'chirildi",
    #             "data":None
    #         }
    #         return Response(data, status=status.HTTP_204_NO_CONTENT)
    #     except Exception as e:
    #         data = {
    #             "success":False,
    #             "message":f"{str(e)}",
    #             'data': None
    #         }
    #         return Response(data, status=status.HTTP_400_BAD_REQUEST)

