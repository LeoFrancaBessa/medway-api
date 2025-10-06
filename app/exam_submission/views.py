from rest_framework.views import APIView
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status
from .services.exam_submission_service import create_exam_submission, get_exam_result
from .serializers import ExamSubmissionCreateSerializer, ExamSubmissionResultSerializer, ExamSubmissionCreateResponseSerializer

class ExamSubmissionAPIView(APIView):
    def post(self, request):
        serializer = ExamSubmissionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        try:
            submission = create_exam_submission(
                student_id=data['student_id'],
                exam_id=data['exam_id'],
                answers=data['answers']
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ExamSubmissionCreateResponseSerializer(submission)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        student_id = request.query_params.get('student_id')
        exam_id = request.query_params.get('exam_id')

        if not student_id or not exam_id:
            return Response({"error": "student_id and exam_id are required"}, status=status.HTTP_400_BAD_REQUEST)

        result = get_exam_result(student_id, exam_id)
        serializer_data = ExamSubmissionResultSerializer(result).data if result else {}
        return Response(serializer_data, status=status.HTTP_200_OK)