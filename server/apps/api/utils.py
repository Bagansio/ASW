from rest_framework.response import Response
from rest_framework import status
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from drf_yasg import openapi
from .core import serializers

def already_exists(queryset, object_name, field, request):
    if len(queryset) > 0:  # exists another submission with url given
        return {
            'message': f'Already exists a submission with that {field}',
            'url_to': reverse(f'{object_name}-detail', args=[queryset[0].id], request=request)
        }
    return None


def get_user(id):
    try:
        return User.objects.get(id=id)

    except Exception as e:
        return None


class ResponseMessages:

    e403 = 'Forbidden.'
    e201_d = 'Deleted.'
    e401 = 'Unauthenticated.'
    e404 = 'Not Found.'
    e409 = 'Already exists.'
    e406 = 'Data is not valid.'


def get_response(message, **kwargs):
    desc = "Error"

    if 'desc' in kwargs:
        desc = kwargs['desc']

    return openapi.Response(
        description=desc,
        examples={
            "application/json": {
                "message": message,
            }
        },
        schema= serializers.MessageSerializer
    )

