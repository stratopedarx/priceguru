# -*- coding: utf-8 -*-
import json
from .forms import AddUrlForm
from django.http import HttpResponse
from django.views.generic import FormView, View, TemplateView
from sceleton import app

as_json = lambda data: json.dumps(data)

class Main(TemplateView):
    template_name = "api/main.html"

    def get_context_data(self, **kwargs):
        kwargs['add_url_form'] = AddUrlForm()
        return kwargs


class AddUrl(View):
    form_class = AddUrlForm

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            task = app.send_task("core.api.tasks.add_url", [form.data['url']])
            return HttpResponse(task.task_id)
        else:
            return HttpResponse(form.errors, status=400)


class CheckTask(View):
    def get(self, request, task_id):
        task = app.AsyncResult(task_id)
        return HttpResponse(as_json(dict(
            ready=task.ready(),
            data=task.result
        )), content_type="application/json")

