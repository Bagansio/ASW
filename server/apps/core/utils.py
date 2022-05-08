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
    submission.save()
    submission.auto_vote()


def saveSubmissionVote(voter,item):

    vote = Vote(voter=voter, submission=item)
    vote.save()
    #item.votes += 1
    changeNumberOfVotes(item, "positive")
    item.save()
    return vote

def deleteSubmissionVote(vote,submission):
    vote.delete()
    changeNumberOfVotes(submission, "negative")
    submission.save()


def changeNumberOfVotes(submission, sign):
    if sign == "positive":
        submission.votes -= 1
    else:
        submission.votes += 1

