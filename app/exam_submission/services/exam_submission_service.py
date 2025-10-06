from django.db import transaction
from ..models import ExamSubmission, ExamSubmissionAnswers
from student.models import Student
from exam.models import Exam, ExamQuestion
from question.models import Question, Alternative


@transaction.atomic #se ocorrer algum erro, rollback
def create_exam_submission(student_id: int, exam_id: int, answers: list):
    try:
        student = Student.objects.get(pk=student_id)
    except Student.DoesNotExist:
        raise ValueError("Student not found")

    try:
        exam = Exam.objects.get(pk=exam_id)
    except Exam.DoesNotExist:
        raise ValueError("Exam not found")
    
    if ExamSubmission.objects.filter(student=student, exam=exam).exists():
        raise ValueError("Submission already exists for this exam and student")
    
    submission = ExamSubmission.objects.create(student=student, exam=exam)
    
    correct_count = 0
    answer_objs = []

    for a in answers:
        question_id = a['question_id']
        answer_id = a['answer_id']
        
        try:
            question = Question.objects.get(pk=question_id)
            answer = Alternative.objects.get(pk=answer_id, question=question)
        except (Question.DoesNotExist, Alternative.DoesNotExist):
            raise ValueError(f"Invalid question/answer: {a}")
        
        if not ExamQuestion.objects.filter(exam=exam, question=question).exists():
            raise ValueError(f"Question not in exam: {a}")
        
        answer_objs.append(
            ExamSubmissionAnswers(
                exam_submission=submission,
                question=question,
                answer=answer
            )
        )
        
        if answer.is_correct:
            correct_count += 1
    
    ExamSubmissionAnswers.objects.bulk_create(answer_objs)

    submission.raw_score = correct_count
    submission.save()
    
    return submission
    

def get_exam_result(student_id: int, exam_id: int):
    
    submission = ExamSubmission.objects.filter(student_id=student_id, exam_id=exam_id).first()
    if not submission:
        return None

    answers_qs = ExamSubmissionAnswers.objects.filter(exam_submission=submission).select_related('question', 'answer')

    answer_list = []
    for a in answers_qs:
        answer_list.append({
            "question_id": a.question.id,
            "question_text": a.question.content,
            "selected_answer_id": a.answer.id,
            "selected_answer_text": a.answer.content,
            "is_correct": a.answer.is_correct
        })

    total_questions = len(answer_list)
    raw_score = submission.raw_score
    percentage = (raw_score / total_questions * 100) if total_questions else 0

    result = {
        "submission_id": submission.id,
        "total_questions": total_questions,
        "raw_score": raw_score,
        "percentage": percentage,
        "answers": answer_list
    }

    return result