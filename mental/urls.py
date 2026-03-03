from django.urls import path

from .views import CreateBoardView, CreateTaskView

urlpatterns = [
    path('createboard/', CreateBoardView.as_view(), name='createboard'),
    path('createtask/', CreateTaskView.as_view(), name='createtask'),
]