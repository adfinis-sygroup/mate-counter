from django.conf.urls import url

from counter import views

urlpatterns = [
    url(r"^$", views.home_view, name="home"),

    url(r'^register/$',
        views.RegistrationView.as_view(),
        name='register'),

    url(r'^send_confirmation_mail/$',
        views.send_confirmation_mail_view,
        name='send confirmation mail')
]
