import sys
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


class Instructor(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    full_time = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class Learner(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    STUDENT = 'student'
    DEVELOPER = 'developer'
    DATA_SCIENTIST = 'data_scientist'
    DATABASE_ADMIN = 'db_admin'
    OCCUPATION_CHOICES = [
        (STUDENT, 'Student'),
        (DEVELOPER, 'Developer'),
        (DATA_SCIENTIST, 'Data Scientist'),
        (DATABASE_ADMIN, 'Database Admin'),
    ]
    occupation = models.CharField(
        max_length=20,
        choices=OCCUPATION_CHOICES,
        default=STUDENT,
    )
    social_link = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.user.username


class Course(models.Model):
    name = models.CharField(max_length=30, null=False, default='online course')
    description = models.CharField(max_length=1000)
    instructors = models.ManyToManyField(Instructor)
    pub_date = models.DateField(null=True)
    total_enrollment = models.IntegerField(default=0)
    is_enrolled = models.BooleanField(default=False)

    def __str__(self):
        return 'Name: ' + self.name + ',' + \
               'Description: ' + self.description


class Lesson(models.Model):
    title = models.CharField(max_length=200, default='')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
    content = models.TextField()


class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    grade = models.IntegerField(default=50)

    def __str__(self):
        return self.question_text

    def is_get_score(self, selected_ids):
        all_answers = self.choice_set.filter(is_correct=True)
        selected_set = set(selected_ids)
        correct_set = set(ans.id for ans in all_answers)
        return selected_set == correct_set


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)


class Enrollment(models.Model):
    AUDIT = 'audit'
    HONOR = 'honor'
    BETA = 'BETA'
    COURSE_MODES = [
        (AUDIT, 'Audit'),
        (HONOR, 'Honor'),
        (BETA, 'BETA'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(default=now)
    mode = models.CharField(max_length=5, choices=COURSE_MODES, default=AUDIT)
    rating = models.FloatField(default=5.0)


class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)
