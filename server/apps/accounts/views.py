from django.shortcuts import render, redirect
from django.views import View
from ..core.models import Submission, Vote
from django.contrib.auth.models import User
from django.http import HttpResponse
from .forms import ProfileForm
from .models import Profile


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
            profile = self.getProfile(user)


            context = {
                'form': ProfileForm(initial={'about': profile.about,
                                             'email': profile.email,
                                             'showdead': profile.showdead,
                                             'noprocrast': profile.noprocrast,
                                             'maxvisit': profile.maxvisit,
                                             'minaway': profile.minaway,
                                             'delay': profile.delay,}),
                'user_searched': user_searched,

            }
            return render(request, 'accounts/profile.html', context)
        else:
            # usuario member
            context = {
                'user_searched': user_searched,
            }

            response = render(request, 'accounts/member.html', context=context)  # render the html with the context

        return HttpResponse(response)

    def post(self, request, username):

        user=request.user
        try:
            user_searched = Profile.objects.get(user=user)

        except Exception as e:
            response = HttpResponse('No such user.')
            return response

        form = ProfileForm(request.POST)
        if form.is_valid():
            form.savedb(user_searched)

        return redirect('profile',username=username)


    def getProfile(self,user):
        try:
            return  Profile.objects.get(user=user)

        except Exception as e:
            profile = Profile(user=user)
            profile.save()
            return profile
