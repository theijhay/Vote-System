from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileUploadSerializer
from .tasks import process_file_task
from django.http import HttpResponse
from celery.result import AsyncResult
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny

"""Simple index view"""
def index(request):
    return HttpResponse("Welcome to the Voter System!")

"""File upload view"""
class FileUploadView(APIView):
    permission_classes = [AllowAny] 
    def post(self, request, *args, **kwargs):
        """Step 1: Validate the file"""
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']

            """Check file format (only allow CSV and Excel files) """
            if not file.name.endswith(('.csv', '.xls', '.xlsx')):
                
                """Return a custom response instead of using ValidationError"""
                return Response({"error": "Invalid file format. Only CSV and Excel files are allowed."},
                                status=status.HTTP_400_BAD_REQUEST)
            
            """Trigger the asynchronous task and get the task_id"""
            task = process_file_task.delay(file.read().decode('utf-8'))  # Pass the file content to Celery
            
            """Return the task ID in the response"""
            return Response({
                "message": "File uploaded and processing started",
                "task_id": task.id  # Celery's task ID
            }, status=status.HTTP_202_ACCEPTED)

        """Return validation errors if the file was not valid"""
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""Task status check view"""
class TaskStatusView(APIView):
    def get(self, request, task_id, *args, **kwargs):
        """Fetch the status of the Celery task using the task_id"""
        task_result = AsyncResult(task_id)
        
        if task_result.state == 'PENDING':
            response = {
                'state': task_result.state,
                'status': 'Task is pending...'
            }
        elif task_result.state != 'FAILURE':
            response = {
                'state': task_result.state,
                'status': 'Task is processing',
                'result': task_result.result  # Include task result if available
            }
        else:
            """If the task failed, return the error traceback"""
            response = {
                'state': task_result.state,
                'status': str(task_result.info)  # This gives the error traceback if task failed
            }
        
        return Response(response)
