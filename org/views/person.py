import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.forms import formset_factory
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape

from org.forms.person import PersonForm, PersonJobFormSet, PersonJobForm
from org.models import Person, City, CompanyFounder, PersonJob


page = 'person'


class PersonCreateView(LoginRequiredMixin, View):
    template_name = 'dashboard/person/person_add.html'
    form_class = PersonForm
    model = Person
    success_url = '/admin/persons'

    def get(self, request, *args, **kwargs):
        form = PersonForm()
        person_job_form_set = PersonJobFormSet(prefix="job")
        context = {
            'page': page,
            'operation': 'Create',
            'form': form,
            'person_job_form_set': person_job_form_set
        }
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = PersonForm(self.request.POST, request.FILES)
        if form.data.get('country'):
            form.fields['city'].queryset = City.objects.filter(country_id=form.data.get('country')).order_by('name')
        person_job_form_set = PersonJobFormSet(self.request.POST, prefix='job')
        form_valid = form.is_valid() and person_job_form_set.is_valid()
        if form_valid:
            person = form.save()
            founded_organizations = form.cleaned_data['founded_organizations']
            for founded_organization in founded_organizations:
                CompanyFounder(person=person, organization=founded_organization).save()
            for person_job_form in person_job_form_set:
                person_job_form.save(person)
            return redirect(self.success_url)
        else:
            context = {
                'page': page,
                'operation': 'Create',
                'form': form,
                'person_job_form_set': person_job_form_set
            }
            return render(request, self.template_name, context)


class PersonUpdateView(LoginRequiredMixin, View):
    template_name = 'dashboard/person/person_add.html'
    form_class = PersonForm
    model = Person
    success_url = '/admin/persons'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        person = Person.objects.get(pk=pk)
        founded_orgs = CompanyFounder.objects.filter(person=person)
        orgs = []
        for f_org in founded_orgs:
            org = f_org.organization
            orgs.append(org)
        # file_data  = {'profile_image': SimpleUploadedFile(person.profile_image)}
        form = PersonForm(initial={'founded_organizations': orgs}, instance=person)

        form.fields['city'].queryset = City.objects.filter(country_id=person.country_id).order_by('name')

        person_job_form = formset_factory(PersonJobForm, extra=0)
        person_job_data = []
        person_jobs = PersonJob.objects.filter(person=person)
        for j in person_jobs:
            person_job_data.append({
                'position': j.position,
                'title': j.person,
                'start_date_year': j.start_date_year,
                'start_date_month': j.start_date_month,
                'start_date_day': j.start_date_day,
                'has_end_date': j.has_end_date,
                'end_date_year': j.end_date_year,
                'end_date_month': j.end_date_month,
                'end_date_day': j.end_date_day,
                'deleted': '0'
            })
        person_job_form_set = person_job_form(initial=person_job_data, prefix="job")
        context = {
            'page': page,
            'operation': 'Update',
            'form': form,
            'person_job_form_set': person_job_form_set,

        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        person = Person.objects.get(pk=pk)
        form = PersonForm(self.request.POST, request.FILES, instance=person)
        if form.data.get('country'):
            form.fields['city'].queryset = City.objects.filter(country_id=form.data.get('country')).order_by('name')
        person_job_form_set = PersonJobFormSet(self.request.POST, prefix='job')
        form_valid = form.is_valid() and person_job_form_set.is_valid()
        if form_valid:
            form.save()

            # delete existing record from CompanyFounder
            CompanyFounder.objects.filter(person=person).delete()
            # entry new record to CompanyFounder
            founded_organizations = form.cleaned_data['founded_organizations']

            for founded_organization in founded_organizations:
                CompanyFounder(person=person, organization=founded_organization).save()

            # delete existing record from PersonJob
            PersonJob.objects.filter(person=person).delete()
            # entry new record to PersonJob
            for person_job_form in person_job_form_set:
                person_job_form.save(person)
            return redirect(self.success_url)
        else:
            context = {
                'page': page,
                'operation': 'Update',
                'form': form,
                'person_job_form_set': person_job_form_set
            }
            return render(request, self.template_name, context)


class PersonListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, "dashboard/person/person_list.html", {'page': page})


class PersonListJson(LoginRequiredMixin, BaseDatatableView):
    model = Person
    # define the columns that will be returned
    columns = ['id', 'first_name', 'last_name', 'city', 'id']
    order_columns = ['first_name', 'first_name', 'city']

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
            city = ""
            if item.city is not None:
                city = item.city.name
            json_data.append([
                escape("{0}".format(str(item.id))),
                escape("{0}".format(item.first_name)),
                escape("{0}".format(item.last_name)),
                escape("{0}".format(city)),
                escape("{0}".format(str(item.id))),
            ])
        return json_data


class PersonDeleteView(LoginRequiredMixin, DeleteView):
    model = Person
    # template_name = "dashboard/person/person_delete.html"
    # success_url = reverse_lazy('person_list')

    def delete(self, request, *args, **kwargs):
        try:
            self.get_object().delete()
            payload = {'status': True}
            return JsonResponse(payload, status=200)
        except Exception as e:
            return JsonResponse({'status': False}, status=500)