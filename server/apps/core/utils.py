from .models import *
from django.utils import timezone


def standardSaveSubmission(author, data):
    submission = Submission(url=data['url'], text=data['text'],
                            title=data['title'])
    saveSubmission(author, submission)

    return submission

def urlSaveSubmission(author, data):

    submission = Submission(title=data['title'], url=data['url'])
    saveSubmission(author, submission)

    return submission

def saveSubmission(author, submission):

    submission.author = author
    submission.created_at = timezone.now()
    submission.votes = 1
    submission.save()
