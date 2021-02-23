from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.shortcuts import render, HttpResponse
from django.views.generic import View


@method_decorator(login_required, name='dispatch')
class HomeView(View):
    template_name = 'ecommerce/home.html'

    def get(self, request, *args, **kwargs) -> 'HttpResponse':

        return render(request, self.template_name, {
            'user': request.user
        })
