from rest_framework import serializers
from .models import Board, Task, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at']
        read_only_fields = ['id','author', 'created_at']


class TaskDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'priority', 'due_date', 'reviewer', 'assignee', 'status', 'comments', 'board']


class CreateBoardSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()

    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ['id', 'title', 'emails', 'members', 'member_count', 'ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count']

    def get_members(self, obj):
        return [ member.user.username for member in obj.members.all() ]


class BoardDetailSerializer(serializers.ModelSerializer):
    tasks = TaskDetailSerializer(many=True, read_only=True)
    members = serializers.SerializerMethodField()

    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()

    def get_member_count(self, obj):
        return obj.members.count()

    def get_ticket_count(self, obj):
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status='to-do').count()

    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority='high').count()

    class Meta:
        model = Board
        fields = ['id', 'title', 'emails', 'tasks', 'members', 'member_count', 'ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count']

    def get_members(self, obj):
        return [ member.user.username for member in obj.members.all() ]



class CreateTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'priority', 'due_date', 'reviewer', 'assignee', 'status', 'comments', 'board']



