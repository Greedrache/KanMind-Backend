from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from mental.models import Board, Task
from .serializers import BoardDetailSerializer, CreateBoardSerializer, CreateTaskSerializer, TaskDetailSerializer
from rest_framework.views import APIView, Response
from rest_framework.permissions import AllowAny
from rest_framework import status


class CreateBoardView(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = CreateBoardSerializer

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
        user = self.request.user
        return Task.objects.filter(assignee=str(user.id))
        
        # Falls du stattdessen den Usernamen im Feld speicherst, nutze stattdessen das hier:
       # return Task.objects.filter(assignee=user.username)