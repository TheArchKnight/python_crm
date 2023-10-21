from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect, reverse

class OrganisorAndLoginRequiredMixin(AccessMixin):
    """Verify the user is auth and is an organisor"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_organisor: 
            return redirect("clientes:lista-cliente")
        return super().dispatch(request, *args, **kwargs)

