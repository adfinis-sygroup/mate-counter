import base64
import os
from django.shortcuts import render
from django.views.generic import FormView
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from counter.forms import RegistrationForm
from counter.models import Profile
from django.views import generic


def home_view(request):
    return render(request, "index.html")


# @login_required
def profile_view(request):

    try:
        current_user = request.user
        profile = Profile.objects.get(user_id=current_user.id)
    except (Profile.DoesNotExist, User.DoesNotExist):
        return render(request, 'no-profile-available.html')

    total = profile.total
    if request.method == 'POST' and request.POST.get('number'):
        total = float(request.POST.get('number')) * float(2)
        Profile.objects.filter(id=profile.id).update(total=total)

    if 'clear all' in request.POST:
        total = 0
        Profile.objects.filter(id=profile.id).update(total=0)

    return render(request,
                  "profile.html", {
                      'current_user': current_user.username,
                      'total': total
                  })


class RegistrationView(FormView):
    model = User
    template_name = 'registration/register.html'
    form_class = RegistrationForm
    success_url = '/send_confirmation_mail'

    def form_valid(self, form):
        user = User.objects.create_user(form.data['username'],
                                        form.data['email'],
                                        form.data['password1'],
                                        first_name=form.data['first_name'],
                                        last_name=form.data['last_name'])
        user.is_active = False
        user.save()

        if user is not None:
            self.generate_profile(user)

        return super(RegistrationView, self).form_valid(form)

    def generate_key(self):
        return base64.b32encode(os.urandom(7))[:10].lower()

    def generate_profile(self, user):
        profile = Profile(key=self.generate_key(), user=user)
        profile.save()
        send_mail(
            'Mate Counter account confirmation',
            """
            Hello,

            please click this link to activate your Mate Counter account:
            {0}/registration_done/{1}

            Sincerely,
            The Mate Counter Team
            """.format(settings.SITE_URL, profile.key.decode("utf-8")),
            'matecounter@matecounter.com',
            [user.email],
            fail_silently=False,
        )


class RegistrationDoneView(generic.TemplateView):
    template_name = 'registration/registration_done.html'

    def get_context_data(request, key):
        matches = Profile.objects.filter(key=key)
        if matches.exists():
            profile = matches.first()
            if profile.user.is_active:
                request.template_name = (
                    'osschallenge/user_is_already_active.html')
            else:
                profile.user.is_active = True
                profile.user.save()
        else:
            request.template_name = 'osschallenge/registration_failed.html'


def send_confirmation_mail_view(request):
    return render(request, "registration/send_confirmation_mail.html")
