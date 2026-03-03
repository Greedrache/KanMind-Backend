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
        
      