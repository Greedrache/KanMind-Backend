from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from mental.models import Board, Task, Comment
from .serializers import BoardDetailSerializer, CommentSerializer, CreateBoardSerializer, CreateTaskSerializer, TaskDetailSerializer
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
        

class TaskCommentView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        # Schritt 1 (GET): Wir suchen in der URL nach der Task-ID (in Django oft "task_pk" genannt)
        task_id = self.kwargs.get('task_pk')
        # Wir filtern die Tabelle: Gib mir nur Kommentare, die zu dieser Task-ID gehören!
        return Comment.objects.filter(task_id=task_id)

    def perform_create(self, serializer):
        # Schritt 2 (POST): Jemand schreibt einen neuen Kommentar.
        task_id = self.kwargs.get('task_pk')
        author = self.request.user.username if self.request.user.is_authenticated else "Gast"
        # Wir speichern ihn in die Datenbank und hängen automatisch die Task-ID und den Namen des Users an!
        serializer.save(task_id=task_id, author=author)