from rest_framework import serializers
from ..models import Board, Task, Comment
from users.models import UserProfile
from django.contrib.auth.models import User


class BoardMemberSerializer(serializers.ModelSerializer): #Member zu einem Board adden
    email = serializers.EmailField(source='user.email', read_only=True)
    fullname = serializers.CharField(source='user.first_name', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'email', 'fullname']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at']
        read_only_fields = ['id','author', 'created_at']


class TaskDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'priority', 'due_date', 'reviewer', 'assignee', 'status', 'comments', 'comments_count', 'board']

    def get_comments_count(self, obj):
        return obj.comments.count()

    def to_representation(self, instance): #Wandelt in JSON um fürs Frontend
        rep = super().to_representation(instance)
        rep['reviewer'] = BoardMemberSerializer(instance.reviewer).data if instance.reviewer else None #Wenn es Existiert, dann wird der Reviewer mit dem BoardMemberSerializer serialisiert, ansonsten wird None zurückgegeben
        rep['assignee'] = BoardMemberSerializer(instance.assignee).data if instance.assignee else None #Wenn es Existiert, dann wird der Assignee mit dem BoardMemberSerializer serialisiert, ansonsten wird None zurückgegeben
        return rep #Gibt Anpassung zurück


class BoardSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()
    owner_id = serializers.PrimaryKeyRelatedField(source='owner', read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'member_count', 'ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id']

    def get_member_count(self, obj):
        return obj.members.count()

    def get_ticket_count(self, obj):
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status='to-do').count()

    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority='high').count()

class CreateBoardSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        required=False,
    )

    class Meta:
        model = Board
        fields = ['id', 'title', 'members']

    def create(self, validated_data):
        users = validated_data.pop('members', [])
        board = Board.objects.create(**validated_data)
        
        if users:
            profiles = []
            for user in users:
                profile, _ = UserProfile.objects.get_or_create(user=user)
                profiles.append(profile)
            board.members.set(profiles)
            
        return board

    def to_representation(self, instance):
        return BoardSerializer(instance).data


class BoardDetailSerializer(serializers.ModelSerializer):
    tasks = TaskDetailSerializer(many=True, read_only=True)
    members = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all(),
        many=True,
        required=False,
    )
    owner_id = serializers.PrimaryKeyRelatedField(source='owner', read_only=True)
    owner_data = BoardMemberSerializer(source='owner', read_only=True)

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
        fields = ['id', 'title', 'emails', 'tasks', 'members', 'member_count', 'ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id', 'owner_data']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['members'] = BoardMemberSerializer(instance.members.all(), many=True).data
        return rep



class CreateTaskSerializer(serializers.ModelSerializer):
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'priority', 'due_date', 'reviewer', 'assignee', 'status', 'comments', 'comments_count', 'board']
        read_only_fields = ['comments'] 

    def get_comments_count(self, obj):
        return obj.comments.count()

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['reviewer'] = BoardMemberSerializer(instance.reviewer).data if instance.reviewer else None
        rep['assignee'] = BoardMemberSerializer(instance.assignee).data if instance.assignee else None
        return rep 


