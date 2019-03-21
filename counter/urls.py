from django.conf.urls import url
from django.contrib.auth import views as auth_views
from counter.forms import LoginForm

from counter import views

urlpatterns = [
    url(r"^$", views.home_view, name="home"),

    url(r'^register/$',
        views.RegistrationView.as_view(),
        name='register'),

    url(r'^registration_done/(?P<key>[\w\.-]+)/',
        views.RegistrationDoneView.as_view(),
        name='registrationdone'),

    url(r'^send_confirmation_mail/$',
        views.send_confirmation_mail_view,
        name='send confirmation mail'),

    url(r'^login/$', auth_views.login, {'authentication_form': LoginForm},
        name='login'),

    url(r'^profile/$', views.profile_view, name='profile'),
]
