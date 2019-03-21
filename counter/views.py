import base64
import os
from django.shortcuts import render
from django.views.generic import FormView
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from counter.forms import RegistrationForm
from counter.models import Profile


def home_view(request):
    return render(request, "index.html")


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
            {}/registration_done/{}

            Sincerely,
            The Mate Counter Team
            """.format(settings.SITE_URL, profile.key),
            'matecounter@matecounter.com',
            [user.email],
            fail_silently=False,
        )


def send_confirmation_mail_view(request):
    return render(request, "registration/send_confirmation_mail.html")
