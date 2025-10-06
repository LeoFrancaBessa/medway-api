from django.db import models
from exam.models import Exam
from question.models import Question, Alternative
from student.models import Student


class ExamSubmission(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    raw_score = models.IntegerField(default=0, help_text="Count of correct answers")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "exam")  


class ExamSubmissionAnswers(models.Model):
    exam_submission = models.ForeignKey(ExamSubmission, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Alternative, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("exam_submission", "question") 