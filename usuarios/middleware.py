from django.shortcuts import redirect
from django.urls import Resolver404, resolve, reverse


class ForcePasswordChangeMiddleware:
    """Redirige al cambio de contraseña en primer login."""

    allowed_url_names = {
        'password_change',
        'password_change_done',
        'logout',
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated and getattr(user, 'debe_cambiar_password', False):
            try:
                match = resolve(request.path_info)
            except Resolver404:
                return self.get_response(request)

            if match.url_name not in self.allowed_url_names and not request.path_info.startswith('/admin/'):
                return redirect(reverse('password_change'))

        return self.get_response(request)
