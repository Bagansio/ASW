from server.apps.comments.models import *
from django.utils import timezone


def create_comment(author, text, submission, level, parent):
    comment = Comment(author=author, text=text, parent=parent,submission=submission,
                      created_at=timezone.now(), level=level)
    comment.save()

    submission.save()
    comment.auto_vote()
    return comment


def saveCommentsVote(voter,item):

    vote = Vote(voter=voter, comment=item)
    vote.save()
    item.votes += 1
    item.save()
