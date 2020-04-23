from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import FormView, UpdateView, CreateView, DeleteView
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from org.forms.acquisition import AcquisitionForm
from org.models import Acquisition
from org.views.helper import get_formatted_date

page = 'acquisition'


class AcquisitionCreateView(LoginRequiredMixin, CreateView):
    template_name = 'dashboard/acquisition/acquisition_add.html'
    form_class = AcquisitionForm
    model = Acquisition
    success_url = '/admin/acquisitions'

    def get_context_data(self, **kwargs):
        ctx = super(AcquisitionCreateView, self).get_context_data(**kwargs)
        ctx['operation'] = 'Create'
        ctx['page'] = 'acquisition'
        return ctx

    def form_valid(self, form):
        a = form.save(commit=False)
        a.transaction_name = a.acquired_organization.name + ' acquired by ' + a.acquiring_organization.name
        a.save()
        return HttpResponseRedirect(self.success_url)


class AcquisitionUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'dashboard/acquisition/acquisition_add.html'
    form_class = AcquisitionForm
    success_url = '/admin/acquisitions'
    model = Acquisition

    def get_context_data(self, **kwargs):
        ctx = super(AcquisitionUpdateView, self).get_context_data(**kwargs)
        ctx['operation'] = 'Update'
        ctx['page'] = 'acquisition'
        return ctx

    def form_valid(self, form):
        a = form.save(commit=False)
        a.transaction_name = a.acquired_organization.name + ' acquired by ' + a.acquiring_organization.name
        a.save()
        return HttpResponseRedirect(self.success_url)


class AcquisitionListView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "dashboard/acquisition/acquisition_list.html", {'page': page})


class AcquisitionListJson(LoginRequiredMixin, BaseDatatableView):
    model = Acquisition
    # define the columns that will be returned
    columns = ['id', 'transaction_name', 'acquiring_organization', 'acquired_organization', 'announced_date_year', 'id']
    order_columns = ['id', 'transaction_name', 'acquiring_organization', 'acquired_organization']

    # def get_initial_queryset(self):
    #     return Event.objects.all()

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

    # def filter_queryset(self, qs):
    #     print(qs)

    def prepare_results(self, qs):
        # prepare list with output column data
        # queryset is already paginated here
        json_data = []
        for item in qs:
            json_data.append([
                escape("{0}".format(str(item.id))),
                escape("{0}".format(item.transaction_name)),
                escape("{0}".format(item.acquiring_organization.name)),
                escape("{0}".format(item.acquired_organization.name)),
                escape(get_formatted_date(item.announced_date_year, item.announced_date_month, item.announced_date_day)),
                escape("{0}".format(str(item.id))),
            ])
        return json_data


class AcquisitionDeleteView(LoginRequiredMixin, DeleteView):
    model = Acquisition
    # template_name = "dashboard/person/person_delete.html"
    # success_url = reverse_lazy('person_list')

    def delete(self, request, *args, **kwargs):
        try:
            self.get_object().delete()
            payload = {'status': True}
            return JsonResponse(payload, status=200)
        except Exception as e:
            print("edsadsd")
            print(e)
            return JsonResponse({'status': False}, status=500)
