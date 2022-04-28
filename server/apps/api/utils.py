from rest_framework.response import Response
from rest_framework import status
from rest_framework.reverse import reverse


def already_exists(queryset, object_name, field, request):
    if len(queryset) > 0:  # exists another submission with url given
        return {
            'message': f'Already exists a submission with that {field}',
            'url_to': reverse(f'{object_name}-detail', args=[queryset[0].id], request=request)
        }
    return None

