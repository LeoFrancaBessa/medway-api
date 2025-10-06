from rest_framework import serializers
from .models import ExamSubmission, ExamSubmissionAnswers

class ExamSubmissionCreateResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamSubmission
        fields = ["id", "exam_id", "student_id", "raw_score", "created_at"]

class ExamAnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    answer_id = serializers.IntegerField()

class ExamSubmissionCreateSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    exam_id = serializers.IntegerField()
    answers = ExamAnswerSerializer(many=True)

class ExamSubmissionAnswerResultSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    question_text = serializers.CharField()
    selected_answer_id = serializers.IntegerField()
    selected_answer_text = serializers.CharField()
    is_correct = serializers.BooleanField()

class ExamSubmissionResultSerializer(serializers.Serializer):
    submission_id = serializers.IntegerField()
    raw_score = serializers.IntegerField()
    total_questions = serializers.IntegerField()
    percentage = serializers.FloatField()
    answers = ExamSubmissionAnswerResultSerializer(many=True)