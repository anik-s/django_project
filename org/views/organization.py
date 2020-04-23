from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.db import transaction
from django.forms import formset_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DeleteView

from org.forms.organization import OrganizationForm, SubOrganizationFormSet, SubOrganizationForm
from org.models import Organization, City, OrganizationHasCategory, OrgSubOrganization


page = 'organization'


class OrganizationCreateView(LoginRequiredMixin, View):
    template_name = 'dashboard/organization/organization_add.html'
    model = Organization
    success_url = '/admin/organizations'

    def get(self, request, *args, **kwargs):
        form = OrganizationForm()
        sub_organization_form_set = SubOrganizationFormSet(prefix="sub_organization")
        context = {
            'page': page,
            'operation': 'Create',
            'form': form,
            'sub_organization_form_set': sub_organization_form_set
        }
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrganizationForm(self.request.POST, request.FILES)
        if form.data.get('country'):
            form.fields['city'].queryset = City.objects.filter(country_id=form.data.get('country')).order_by('name')
        sub_organization_form_set = SubOrganizationFormSet(self.request.POST, prefix='sub_organization')
        form_valid = form.is_valid() and sub_organization_form_set.is_valid()
        if form_valid:
            organization = form.save()
            industry_categories = form.cleaned_data['industry_categories']
            for ic in industry_categories:
                OrganizationHasCategory(organization=organization, category_id=ic).save()
            for sub_organization_form in sub_organization_form_set:
                sub_organization_form.save(organization)
            return redirect(self.success_url)
        else:
            context = {
                'page': page,
                'operation': 'Create',
                'form': form,
                'sub_organization_form_set': sub_organization_form_set
            }
            return render(request, self.template_name, context)


class OrganizationUpdateView(LoginRequiredMixin, View):
    template_name = 'dashboard/organization/organization_add.html'
    model = Organization
    success_url = '/admin/organizations'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        organization = Organization.objects.get(pk=pk)
        industry_categories = OrganizationHasCategory.objects.filter(organization=organization)
        existing = []
        for ic in industry_categories:
            existing.append(str(ic.category_id))
        form = OrganizationForm(initial={'industry_categories': existing}, instance=organization)
        form.fields['city'].queryset = City.objects.filter(country_id=organization.country_id).order_by('name')

        sub_organization_form = formset_factory(SubOrganizationForm, extra=0)
        sub_organization_data = []
        org_sub_organizations = OrgSubOrganization.objects.filter(organization=organization)
        for oso in org_sub_organizations:
            sub_organization_data.append({
                'organization': oso.sub_organization,
                'relation': oso.relation,
                'deleted': '0'
            })
        sub_organization_form_set = sub_organization_form(initial=sub_organization_data, prefix="sub_organization")
        context = {
            'page': page,
            'operation': 'Update',
            'form': form,
            'sub_organization_form_set': sub_organization_form_set
        }
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        organization = Organization.objects.get(pk=pk)
        form = OrganizationForm(self.request.POST, request.FILES, instance=organization)
        sub_organization_form_set = SubOrganizationFormSet(self.request.POST, prefix='sub_organization')
        form_valid = form.is_valid() and sub_organization_form_set.is_valid()
        if form_valid:
            organization = form.save()
            # delete existing record from OrganizationHasCategory
            OrganizationHasCategory.objects.filter(organization=organization).delete()
            industry_categories = form.cleaned_data['industry_categories']
            # entry new record to OrganizationHasCategory
            for ic in industry_categories:
                OrganizationHasCategory(organization=organization, category_id=ic).save()

            # delete existing record from OrgSubOrganization
            OrgSubOrganization.objects.filter(organization=organization).delete()
            # entry new record to OrgSubOrganization
            for sub_organization_form in sub_organization_form_set:
                sub_organization_form.save(organization)
            return redirect(self.success_url)
        else:
            context = {
                'page': page,
                'operation': 'Update',
                'form': form,
                'sub_organization_form_set': sub_organization_form_set
            }
            return render(request, self.template_name, context)


class OrganizationListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, "dashboard/organization/organization_list.html", {'page': page})


from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape


class OrganizationListJson(LoginRequiredMixin, BaseDatatableView):
    model = Organization
    # define the columns that will be returned
    columns = ['id', 'name', 'organization_type', 'id']
    order_columns = ['name', 'organization_type']

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
            json_data.append([
                escape("{0}".format(str(item.id))),
                escape("{0}".format(item.name)),
                escape("{0}".format(item.organization_type)),
                escape("{0}".format(str(item.id))),
            ])
        return json_data


class OrganizationDeleteView(LoginRequiredMixin, DeleteView):
    model = Organization
    # template_name = "dashboard/person/person_delete.html"
    # success_url = reverse_lazy('person_list')

    def delete(self, request, *args, **kwargs):
        try:
            self.get_object().delete()
            payload = {'status': True}
            return JsonResponse(payload, status=200)
        except Exception as e:
            return JsonResponse({'status': False}, status=500)
