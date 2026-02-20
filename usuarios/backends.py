from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class DNIMailBackend(ModelBackend):
    """
    Permite autenticación con DNI + contraseña.
    """

    def authenticate(self, request, dni=None, password=None, **kwargs):
        UserModel = get_user_model()
        dni = dni or kwargs.get(UserModel.USERNAME_FIELD) or kwargs.get('username')

        if not dni or not password:
            return None

        try:
            user = UserModel.objects.get(dni=dni)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
