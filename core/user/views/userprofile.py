# coding: utf-8
import json
from django.db.models import F, Count, Func, Value, FloatField
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.http import JsonResponse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View, TemplateView


from core.api.models import ItemGroup, UserItem
from core.user.forms.userprofile import AddUserItemIntoGroupForm
from core.user.views.user import LoginRequiredMixin
from sceleton import app


class AjaxableResponseUpdateMixin(UpdateView):
    """
    Mixin to add AJAX support to a form.
    Based on UpdateView
    """
    redirect_to = '/'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        return JsonResponse({'status': '200 OK'}, status=200)

    def form_invalid(self, form):
        response = super(AjaxableResponseUpdateMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'text': 'It\'s ajax method'})

class AjaxableResponseCreateMixin(CreateView):
    """
    Mixin to add AJAX support to a form.
    Based on CreateView
    """
    redirect_to = '/'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        return JsonResponse({'status': '200 OK'}, status=200)

    def form_invalid(self, form):
        response = super(AjaxableResponseCreateMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response


    def form_valid(self, form):
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'text': 'It\'s ajax method'})

class UserProfileView(LoginRequiredMixin, ListView):

    """Show list of groups on the userpage."""

    template_name = 'userprofile/home.html'
    model = ItemGroup

    def get_queryset(self):
        qs = super(UserProfileView, self).get_queryset()
        return qs.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        groups = ItemGroup.objects.filter(user=self.request.user).annotate(itemscount=Count('useritem'))
        context['currency'] = self.request.COOKIES.get('currency')
        for g in groups:
            g.items = list(set(UserItem.objects.filter(group__id=g.id).annotate(
                itemprice_id=F('item__itemprice'),
                current_price_converted=F('item__itemprice__current_price') * Func('item__itemprice__currency',
                                                                                   Value(context['currency']),
                                                                                   function='get_currency_ratio',
                                                                                   output_field=FloatField()),
                price_created_date=F('item__itemprice__created_date'),
                url=F('item__url'),
                partner_name=F('item__source__partner__name')).order_by('-price_created_date')))

        context['groups'] = groups
        return context


class UserProfileItemGroupView(LoginRequiredMixin, DetailView):
    """Show list of items for the given group."""

    template_name = 'userprofile/itemgroup.html'
    model = ItemGroup
    context_object_name = 'group'
    form_class = AddUserItemIntoGroupForm

    def get_context_data(self, **kwargs):
        context = super(UserProfileItemGroupView, self).get_context_data(**kwargs)
        add_item_form = self.form_class(initial={'group_id': self.kwargs['pk']})
        context['currency'] = self.request.COOKIES.get('currency')
        context['group'].items = list(set(UserItem.objects.filter(group__id=context['group'].id).annotate(
                current_price_converted=F('item__itemprice__current_price') * Func('item__itemprice__currency',
                                                                                   Value(context['currency']),
                                                                                   function='get_currency_ratio',
                                                                                   output_field=FloatField()),
                price_created_date=F('item__itemprice__created_date'),
                url=F('item__url'),
                partner_name=F('item__source__partner__name')).order_by('-price_created_date')))
        context['add_item_form'] = add_item_form
        context['is_show_itemgroup'] = True
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            group_id = form.cleaned_data['group_id']
            url = form.cleaned_data['url']
            task = app.send_task('core.api.tasks.add_useritem_into_group', args=[url, group_id])
            return HttpResponse(task.id)
        else:
            return HttpResponseBadRequest('URL is invalid!')


class ItemGroupCreateViewAjax(LoginRequiredMixin, AjaxableResponseCreateMixin):
    model = ItemGroup
    fields = ['group_name']

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super(AjaxableResponseCreateMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'id': self.object.pk,
                'text': u'Группа успешно добавлена',
                'group_name': self.object.group_name,
            }
            return JsonResponse(data)
        else:
            return response


class ItemGroupUpdateViewAjax(LoginRequiredMixin, AjaxableResponseUpdateMixin):
    model = ItemGroup
    fields = ['group_name']

    def get_object(self):
        try:
            obj = ItemGroup.objects.get(id=int(self.request.POST['pk']), user=self.request.user)
        except ItemGroup.DoesNotExist:
            return HttpResponse(u"Object not found", status=404)
        else:
            return obj

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super(AjaxableResponseUpdateMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'id': self.object.pk,
                'text': u'Группа успешно обновлена',
                'group_name': self.object.group_name,
            }
            return JsonResponse(data)
        else:
            return response


class ItemGroupCreateView(LoginRequiredMixin, CreateView):
    model = ItemGroup
    fields = ['group_name']
    template_name = 'userprofile/itemgroup_form.html'
    success_url = reverse_lazy('user:userprofile')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ItemGroupCreateView, self).form_valid(form)


class ItemGroupDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'userprofile/itemgroup_confirm_delete.html'
    model = ItemGroup
    success_url = reverse_lazy('user:userprofile')


class UserItemUpdateView(LoginRequiredMixin, UpdateView):
    model = UserItem
    fields = ['custom_name']
    template_name = 'userprofile/useritem_form.html'

    def get_success_url(self):
        return reverse_lazy('user:itemgroup', args=[self.object.group.pk])

class UserItemDeleteViewAjax(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request):
        UserItem.objects.filter(id__in=request.POST.getlist('items[]'), group__user=request.user).delete()
        return JsonResponse({'status': u'OK', 'text': u'Items were deleted'}, status=200)

class UserItemEditViewAjax(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request):
        for k, v in request.POST.items():
            UserItem.objects.filter(id=k, group__user=request.user).update(custom_name=v)


        return JsonResponse({'status': 'OK'}, status=200)

class UserItemDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'userprofile/useritem_confirm_delete.html'
    model = UserItem

    def get_success_url(self):
        return reverse_lazy('user:itemgroup', args=[self.object.group.pk])
