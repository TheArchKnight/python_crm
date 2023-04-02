from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

class EmpleadoRequiredMixin(AccessMixin):
    """Verify the user has acces to the clients app"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.fumigacion:
            return redirect(("landing-page"))
        return super().dispatch(request, *args, **kwargs)


