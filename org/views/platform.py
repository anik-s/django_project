from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DeleteView
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape

from org.forms.platform import PlatformForm
from org.models import Platform, PlatformCategory


page = 'platform'


class PlatformCreateView(LoginRequiredMixin, View):
    template_name = 'dashboard/platform/platform_add.html'
    form_class = PlatformForm
    model = Platform
    success_url = '/admin/platforms'

    def get(self, request, *args, **kwargs):
        form = PlatformForm()
        context = {
            'page': page,
            'operation': 'Create',
            'form': form
        }
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = PlatformForm(self.request.POST, request.FILES)
        if form.is_valid():
            platform = form.save()
            industry_categories = form.cleaned_data['industry_categories']
            for ic in industry_categories:
                PlatformCategory(platform=platform, category_id=ic).save()
            return redirect(self.success_url)
        else:
            context = {
                'page': page,
                'operation': 'Create',
                'form': form
            }
            return render(request, self.template_name, context)


class PlatformUpdateView(LoginRequiredMixin, View):
    template_name = 'dashboard/platform/platform_add.html'
    model = Platform
    success_url = '/admin/platforms'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        platform = Platform.objects.get(pk=pk)
        industry_categories = PlatformCategory.objects.filter(platform=platform)
        existing = []
        for ic in industry_categories:
            existing.append(str(ic.category_id))
        form = PlatformForm(initial={'industry_categories': existing}, instance=platform)
        context = {
            'page': page,
            'operation': 'Update',
            'form': form
        }
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        platform = Platform.objects.get(pk=pk)
        form = PlatformForm(self.request.POST, request.FILES, instance=platform)
        if form.is_valid():
            platform = form.save()
            # delete existing record from PlatformCategory
            PlatformCategory.objects.filter(platform=platform).delete()
            industry_categories = form.cleaned_data['industry_categories']
            # entry new record to PlatformCategory
            for ic in industry_categories:
                PlatformCategory(platform=platform, category_id=ic).save()
            return redirect(self.success_url)
        else:
            context = {
                'page': page,
                'operation': 'Update',
                'form': form
            }
            return render(request, self.template_name, context)


class PlatformListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, "dashboard/platform/platform_list.html", {'page': page})


class PlatformListJson(LoginRequiredMixin, BaseDatatableView):
    model = Platform
    # define the columns that will be returned
    columns = ['id', 'name', 'platform_business_model_type', 'id']
    order_columns = ['name', 'platform_business_model_type']

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 50

    # def render_column(self, row, column):
    #     # We want to render user as a custom column
    #     # if column == 'user':
    #     #     # escape HTML for security reasons
    #     #     return escape('{0} {1}'.format(row.first_name, row.first_name))
    #     # else:
    #     return super(PersonListJson, self).render_column(row, column)

    def prepare_results(self, qs):
        # prepare list with output column data
        # queryset is already paginated here
        json_data = []
        for item in qs:
            t = ""
            if item.platform_business_model_type is not None:
                t = item.platform_business_model_type.name
            json_data.append([
                escape("{0}".format(str(item.id))),
                escape("{0}".format(item.name)),
                escape("{0}".format(t)),
                escape("{0}".format(str(item.id))),
            ])
        return json_data


class PlatformDeleteView(LoginRequiredMixin, DeleteView):
    model = Platform
    # template_name = "dashboard/person/person_delete.html"
    # success_url = reverse_lazy('person_list')

    def delete(self, request, *args, **kwargs):
        try:
            self.get_object().delete()
            payload = {'status': True}
            return JsonResponse(payload, status=200)
        except Exception as e:
            return JsonResponse({'status': False}, status=500)