from rest_framework import serializers
from .models import Board, Task






class TaskDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'priority', 'due_date', 'reviewer', 'assignee', 'status', 'board']


class CreateBoardSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ['id', 'title', 'emails', 'members']

    def get_members(self, obj):
        return [ member.user.username for member in obj.members.all() ]


class BoardDetailSerializer(serializers.ModelSerializer):
    tasks = TaskDetailSerializer(many=True, read_only=True)
    members = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ['id', 'title', 'emails', 'tasks', 'members']

    def get_members(self, obj):
        return [ member.user.username for member in obj.members.all() ]



class CreateTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'priority', 'due_date', 'reviewer', 'assignee', 'status', 'board']



