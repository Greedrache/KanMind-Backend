from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from django.db.models import Q
from mental.models import Board, Task, Comment
from .serializers import BoardDetailSerializer, CommentSerializer, CreateBoardSerializer, CreateTaskSerializer, TaskDetailSerializer, BoardSerializer
from rest_framework.views import APIView, Response
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework import status

from django.contrib.auth.models import User
from users.models import UserProfile


class CreateBoardView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        profile, _ = UserProfile.objects.get_or_create(user=user)
        return Board.objects.filter(Q(owner=profile) | Q(members=profile)).distinct()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BoardSerializer
        return CreateBoardSerializer

    def perform_create(self, serializer):
        profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
        serializer.save(owner=profile)


class IsBoardMemberOrOwner(BasePermission):
    message = 'forbidden' #When the user is not authenticated or not a member/owner of the board, this message will be returned in the response :)

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        return obj.owner == profile or obj.members.filter(id=profile.id).exists()


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardDetailSerializer
    permission_classes = [IsAuthenticated, IsBoardMemberOrOwner]



class CreateTaskView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = CreateTaskSerializer


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer



class AssignedTasksView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskDetailSerializer

    def get_queryset(self):
        profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
        return Task.objects.filter(assignee=profile)
        



class ReviewTasksView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskDetailSerializer

    def get_queryset(self):
        profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
        return Task.objects.filter(reviewer=profile)
        

class TaskCommentView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        task_id = self.kwargs.get('task_pk')
        return Comment.objects.filter(task_id=task_id) #Gibt nur die Kommentare die zu dem Task gehören zurück

    def perform_create(self, serializer):
        task_id = self.kwargs.get('task_pk')
        author = self.request.user.first_name if self.request.user.is_authenticated else "Gast"
        serializer.save(task_id=task_id, author=author)



class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_update(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(author=self.request.user.first_name)
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
                'fullname': user.first_name,
            },
            status=status.HTTP_200_OK,
        )