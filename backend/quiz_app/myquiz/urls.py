from django.urls import path,include

from .views import (
    add_quiz,add_question,delete_question,view_quiz_questions,
    quiz_in_a_course_list,make_a_quiz_submission,view_quiz_marks_list,
    calculate_all_student_marks,delete_a_quiz,delete_a_course
)

urlpatterns = [
	path('add/',add_quiz, name="add_quiz"),
	path('question/add/',add_question, name="add_question"),
	path('question/delete/',delete_question, name="delete_question"),
	path('view/<int:course_pk>/<int:quiz_pk>/',view_quiz_questions, name="view_quiz_questions"),
	path('view/<int:course_pk>/',quiz_in_a_course_list, name="quiz_in_a_course_list"),
	path('make/submission/',make_a_quiz_submission, name="make_a_quiz_submission"),
	path('show/marks/list/<int:course_pk>/<int:quiz_pk>/',view_quiz_marks_list, name="view_quiz_marks_list"),
	path('marks/calculate/',calculate_all_student_marks,name="calculate_all_student_marks"),
	path('delete/',delete_a_quiz,name="delete_a_quiz"),
	path('delete/course/',delete_a_course,name="delete_a_course"),
]