from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic import RedirectView

from usuarios.views import PrimerLoginPasswordChangeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path(
        'accounts/password/change/',
        PrimerLoginPasswordChangeView.as_view(template_name='registration/password_change.html'),
        name='password_change',
    ),
    path(
        'accounts/password/change/done/',
        auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
        name='password_change_done',
    ),
    path('', RedirectView.as_view(pattern_name='usuarios:carrera-list', permanent=False)),
    path('', include('usuarios.urls')),
]
