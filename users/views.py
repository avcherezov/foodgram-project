from django.views.generic import CreateView
from .forms import UserForm
from django.urls import reverse_lazy


class SignUp(CreateView):
    form_class = UserForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"
