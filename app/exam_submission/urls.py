from django.urls import path
from .views import ExamSubmissionAPIView

urlpatterns = [
    path('exam_submission/', ExamSubmissionAPIView.as_view(), name='exam_submission'),
]