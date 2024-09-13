from django.urls import path
from .views import FileUploadView, index
from .views import FileUploadView, TaskStatusView

urlpatterns = [
    path('', index, name='voters-index'),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('task-status/<str:task_id>/', TaskStatusView.as_view(), name='task-status'),
]
