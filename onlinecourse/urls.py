from django.urls import path
from . import views

app_name = 'onlinecourse'
urlpatterns = [
    # ex: /onlinecourse/
    path('', views.CourseListView.as_view(), name='index'),
    # ex: /onlinecourse/5/
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course_details'),
    # ex: /onlinecourse/5/enroll/
    path('<int:course_id>/enroll/', views.enroll, name='enroll'),
    # ex: /onlinecourse/5/submit/
    path('<int:course_id>/submit/', views.submit, name='submit'),
    # ex: /onlinecourse/5/exam_result/3/
    path('<int:course_id>/exam_result/<int:submission_id>/', views.show_exam_result, name='exam_result'),
]
