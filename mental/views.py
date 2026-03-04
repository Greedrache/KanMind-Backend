from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from mental.models import Board, Task, Comment
from .serializers import BoardDetailSerializer, CommentSerializer, CreateBoardSerializer, CreateTaskSerializer, TaskDetailSerializer
from rest_framework.views import APIView, Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from django.contrib.auth.models import User
from users.models import UserProfile


class CreateBoardView(generics.ListCreateAPIView):
    queryset = Board.objects.all()

    def get_serializer_class(self):
        # Wenn wir nur lesen (GET), liefern wir alles im Detail aus:
        if self.request.method == 'GET':
            return BoardDetailSerializer
        # Für alle anderen (wie POST), nehmen wir den normalen:
        return CreateBoardSerializer


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardDetailSerializer



class CreateTaskView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = CreateTaskSerializer


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer



class AssignedTasksView(generics.ListAPIView):
    serializer_class = TaskDetailSerializer

    def get_queryset(self):
        return Task.objects.all()
        



class ReviewTasksView(generics.ListAPIView):
    serializer_class = TaskDetailSerializer

    def get_queryset(self):
        return Task.objects.all()
        

class TaskCommentView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        task_id = self.kwargs.get('task_pk')
        return Comment.objects.filter(task_id=task_id) #Gibt nur die Kommentare die zu dem Task gehören zurück

    def perform_create(self, serializer):
        task_id = self.kwargs.get('task_pk')
        author = self.request.user.username if self.request.user.is_authenticated else "Gast"
        serializer.save(task_id=task_id, author=author)



class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_update(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(author=self.request.user.username)
        else:
            serializer.save(author="Gast")


class EmailCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        email = (request.query_params.get('email') or '').strip()
        if not email:
            return Response({'detail': 'Query parameter "email" is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'No user with this email.'}, status=status.HTTP_404_NOT_FOUND)
        profile, _created = UserProfile.objects.get_or_create(user=user)
        return Response(
            {
                'id': profile.id,
                'email': user.email,
                'fullname': user.username,
            },
            status=status.HTTP_200_OK,
        )