from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class DNIMailBackend(ModelBackend):
    """
    Permite autenticación con DNI + email + contraseña.
    """

    def authenticate(self, request, dni=None, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        dni = dni or kwargs.get(UserModel.USERNAME_FIELD)
        email = email or kwargs.get('email')

        if not dni or not email or not password:
            return None

        try:
            user = UserModel.objects.get(dni=dni, email__iexact=email)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
