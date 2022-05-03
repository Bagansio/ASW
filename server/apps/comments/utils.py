from server.apps.comments.models import *
from django.utils import timezone


def create_comment(author, text, submission, level, parent):
    comment = Comment(author=author, text=text, parent=parent,submission=submission,
                      created_at=timezone.now(), level=level)
    comment.save()

    submission.save()
    comment.auto_vote()
    return comment
