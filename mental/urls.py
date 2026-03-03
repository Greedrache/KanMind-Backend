from django.urls import path

from .views import CreateBoardView, BoardDetailView, CreateTaskView

urlpatterns = [
    path('boards/', CreateBoardView.as_view(), name='createboard'),
    path('boards/<int:pk>/', BoardDetailView.as_view(), name='board-detail'),
    path('createtask/', CreateTaskView.as_view(), name='createtask'),
]