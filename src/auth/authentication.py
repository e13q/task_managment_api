from rest_framework.authentication import TokenAuthentication, SessionAuthentication


class UpdateIPMixin:
    def _update_ip(self, request, user):
        ip = self._get_client_ip(request)
        if user.api_last_ip != ip:
            user.api_last_ip = ip
            user.save(update_fields=['api_last_ip'])

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def authenticate(self, request):
        res = super().authenticate(request)
        if res:
            user, _ = res
            if user.is_authenticated:
                self._update_ip(request, user)
        return res


class SaveIPTokenAuthentication(UpdateIPMixin, TokenAuthentication):
    pass


class SaveIPSessionAuthentication(UpdateIPMixin, SessionAuthentication):
    pass
