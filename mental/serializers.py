from rest_framework import serializers
from .models import Board, Task



class CreateBoardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Board
        fields = ['title', 'emails']



class CreateTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'date', 'board']