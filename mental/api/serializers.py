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
    assignee = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all(),
        allow_null=True,
        required=False,
        error_messages={'does_not_exist': 'The specified assignee does not exist.'}
    )
    reviewer = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all(),
        allow_null=True,
        required=False,
        error_messages={'does_not_exist': 'The specified reviewer does not exist.'}
    )
    assignee_id = serializers.PrimaryKeyRelatedField(
        source='assignee',
        queryset=UserProfile.objects.all(),
        allow_null=True,
        required=False,
        write_only=True,
        error_messages={'does_not_exist': 'The specified assignee does not exist.'}
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        source='reviewer',
        queryset=UserProfile.objects.all(),
        allow_null=True,
        required=False,
        write_only=True,
        error_messages={'does_not_exist': 'The specified reviewer does not exist.'}
    )

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'priority', 'due_date', 'reviewer', 'reviewer_id', 'assignee', 'assignee_id', 'status', 'comments', 'comments_count', 'board']

    def get_comments_count(self, obj):
        return obj.comments.count()

    def to_representation(self, instance): #Wandelt in JSON um fürs Frontend
        rep = super().to_representation(instance)
        rep['reviewer'] = BoardMemberSerializer(instance.reviewer).data if instance.reviewer else None
        rep['assignee'] = BoardMemberSerializer(instance.assignee).data if instance.assignee else None
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
        rep['members_data'] = BoardMemberSerializer(instance.members.all(), many=True).data #umbenenannt zu members_data damit es bei Postman nicht zu Verwirrung kommt, da es ja eigentlich die IDs der Mitglieder sein sollten, aber hier werden die Daten der Mitglieder zurückgegeben
        if 'members' in rep:
            del rep['members']
        return rep



class CreateTaskSerializer(serializers.ModelSerializer):
    comments_count = serializers.SerializerMethodField()
    board = serializers.PrimaryKeyRelatedField(
        queryset=Board.objects.all(),
        error_messages={'does_not_exist': 'This Board does not exist.'}
    )
    assignee = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all(),
        allow_null=True,
        required=False,
        error_messages={'does_not_exist': 'The specified assignee does not exist.'}
    )
    reviewer = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all(),
        allow_null=True,
        required=False,
        error_messages={'does_not_exist': 'The specified reviewer does not exist.'}
    )
    assignee_id = serializers.PrimaryKeyRelatedField(
        source='assignee',
        queryset=UserProfile.objects.all(),
        allow_null=True,
        required=False,
        write_only=True,
        error_messages={'does_not_exist': 'The specified assignee does not exist.'}
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        source='reviewer',
        queryset=UserProfile.objects.all(),
        allow_null=True,
        required=False,
        write_only=True,
        error_messages={'does_not_exist': 'The specified reviewer does not exist.'}
    )

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'priority', 'due_date', 'reviewer', 'reviewer_id', 'assignee', 'assignee_id', 'status', 'comments', 'comments_count', 'board']
        read_only_fields = ['comments'] 

    def get_comments_count(self, obj):
        return obj.comments.count()

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['reviewer'] = BoardMemberSerializer(instance.reviewer).data if instance.reviewer else None
        rep['assignee'] = BoardMemberSerializer(instance.assignee).data if instance.assignee else None
        return rep 


