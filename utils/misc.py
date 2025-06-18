from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.exceptions import ValidationError

User = get_user_model()


def querydict_to_dict(query_dict):
    data = {}
    for key in query_dict.keys():
        v = query_dict.getlist(key)
        if len(v) == 1:
            v = v[0]
        data[key] = v
    return data


def get_user_by_uidb64(uidb64):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
        user = None
    return user


def create_user_activation_link(user, request):
    confirmation_token = default_token_generator.make_token(user)
    activation_link = (f'{request.scheme}://{request.get_host()}/activate-user/'
                       f'{urlsafe_base64_encode(force_bytes(user.pk))}-_-{confirmation_token}/')
    return activation_link
