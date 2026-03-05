from django.urls import path

from .views import (
    AssignedTasksView,
    BoardDetailView,
    CommentDetailView,
    CreateBoardView,
    CreateTaskView,
    EmailCheckView,
    ReviewTasksView,
    TaskCommentView,
    TaskDetailView,
)

urlpatterns = [
    path('boards/', CreateBoardView.as_view(), name='createboard'),
    path('boards/<int:pk>/', BoardDetailView.as_view(), name='board-detail'),
    path('email-check/', EmailCheckView.as_view(), name='email-check'),
    path('tasks/', CreateTaskView.as_view(), name='createtask'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/assigned-to-me/', AssignedTasksView.as_view(), name='assigned-tasks'),
    path('tasks/reviewing/', ReviewTasksView.as_view(), name='reviewing-tasks'),
    path('tasks/<int:task_pk>/comments/', TaskCommentView.as_view(), name='task-comments'),#
    path('tasks/<int:task_pk>/comments/<int:pk>/', CommentDetailView.as_view(), name='task-comment-detail'),
]
