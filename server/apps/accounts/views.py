from django.shortcuts import render, redirect
from django.views import View
from ..core.models import Submission, Vote
from django.contrib.auth.models import User
from django.http import HttpResponse


# profile/<username> view


class ProfileView(View):

    def get(self, request, username):
        user = request.user
        response = HttpResponse('No such user.')
        try:
            user_searched = User.objects.get(username=username)

        except Exception as e:
            return response

        if user == user_searched:
            #usuario logeado
            print("not implemented")
        else:
            # usuario member
            context = {
                'user_searched': user_searched,
            }

            response = render(request, 'accounts/member.html', context=context)  # render the html with the context

        return HttpResponse(response)
