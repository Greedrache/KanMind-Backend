from django.urls import path

from .views import AssignedTasksView, CreateBoardView, BoardDetailView, CreateTaskView, ReviewTasksView, TaskCommentView, TaskDetailView

urlpatterns = [
    path('boards/', CreateBoardView.as_view(), name='createboard'),
    path('boards/<int:pk>/', BoardDetailView.as_view(), name='board-detail'),
    path('tasks/', CreateTaskView.as_view(), name='createtask'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/assigned-to-me/', AssignedTasksView.as_view(), name='assigned-tasks'),
    path('tasks/reviewing/', ReviewTasksView.as_view(), name='reviewing-tasks'),
    path('tasks/<int:task_pk>/comments/', TaskCommentView.as_view(), name='task-comments'),
]
