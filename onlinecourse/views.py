from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import Course, Lesson, Enrollment, Question, Choice, Submission

def submit(request, course_id):
    enrollment = Enrollment.objects.filter(user=request.user, course_id=course_id).first()
    if request.method == 'POST':
        selected_ids = request.POST.getlist('choice')
        submission = Submission.objects.create(enrollment=enrollment)
        for choice_id in selected_ids:
            choice = Choice.objects.get(pk=choice_id)
            submission.choices.add(choice)
        return HttpResponseRedirect(reverse('onlinecourse:exam_result', args=(course_id, submission.id)))
    return redirect('onlinecourse:course_details', course_id=course_id)

def show_exam_result(request, course_id, submission_id):
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    selected_choices = submission.choices.all()
    
    total_score = 0
    questions = Question.objects.filter(course=course)
    for question in questions:
        if question.is_get_score(selected_choices.values_list('id', flat=True)):
            total_score += question.grade

    context['course'] = course
    context['submission'] = submission
    context['selected_choices'] = selected_choices
    context['grade'] = total_score
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
