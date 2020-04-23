from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.forms import formset_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DeleteView
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape

from org.forms.funding_round import FundingRoundForm, InvestorFormSet, InvestorForm
from org.models import FundingRound, FundingRoundInvestor, FundingRoundInvestorOrganization
from org.views.helper import get_formatted_date

page = 'funding_round'


class FundingRoundCreateView(LoginRequiredMixin, View):
    template_name = 'dashboard/funding_round/funding_round_add.html'
    model = FundingRound
    success_url = '/admin/funding_rounds'

    def get(self, request, *args, **kwargs):
        form = FundingRoundForm()
        investor_form_set = InvestorFormSet(prefix="investor")
        context = {
            'page': page,
            'operation': 'Create',
            'form': form,
            'investor_form_set': investor_form_set
        }
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = FundingRoundForm(self.request.POST)
        investor_form_set = InvestorFormSet(self.request.POST, prefix='investor')
        form_valid = form.is_valid() and investor_form_set.is_valid()
        if form_valid:
            funding_round = form.save()
            for investor_form in investor_form_set:
                investor_form.save(funding_round)
            return redirect(self.success_url)
        else:
            context = {
                'operation': 'Create',
                'page': page,
                'form': form,
                'investor_form_set': investor_form_set
            }
            return render(request, self.template_name, context)


class FundingRoundUpdateView(LoginRequiredMixin, View):
    template_name = 'dashboard/funding_round/funding_round_add.html'
    model = FundingRound
    success_url = '/admin/funding_rounds'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        funding_round = FundingRound.objects.get(pk=pk)
        form = FundingRoundForm(instance=funding_round)
        investor_form = formset_factory(InvestorForm, extra=0)
        investor_data = []
        investors = FundingRoundInvestor.objects.filter(funding_round=funding_round)
        for i in investors:
            investor_data.append({
                'investor_type': 'person',
                'person': i.person,
                'lead_investor': i.lead_investor,
                'money_raised': i.money_raised,
                'money_raised_currency': i.money_raised_currency
            })
        investor_orgs = FundingRoundInvestorOrganization.objects.filter(funding_round=funding_round)
        for io in investor_orgs:
            investor_data.append({
                'investor_type': 'organization',
                'organization': io.investor_organization,
                'lead_investor': io.lead_investor,
                'money_raised': io.money_raised,
                'money_raised_currency': io.money_raised_currency
            })
        investor_form_set = investor_form(initial=investor_data, prefix="investor")
        context = {
            'operation': 'Update',
            'page': page,
            'form': form,
            'investor_form_set': investor_form_set
        }
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        funding_round = FundingRound.objects.get(pk=pk)
        form = FundingRoundForm(self.request.POST, instance=funding_round)
        investor_form_set = InvestorFormSet(self.request.POST, prefix='investor')
        print(investor_form_set.errors)
        form_valid = form.is_valid() and investor_form_set.is_valid()
        if form_valid:
            funding_round = form.save()
            # delete existing record from FundingRoundInvestor and FundingRoundInvestorOrganization
            FundingRoundInvestor.objects.filter(funding_round=funding_round).delete()
            FundingRoundInvestorOrganization.objects.filter(funding_round=funding_round).delete()
            # entry new record to FundingRoundInvestor and FundingRoundInvestorOrganization
            for investor_form in investor_form_set:
                investor_form.save(funding_round)
            return redirect(self.success_url)
        else:
            context = {
                'operation': 'Update',
                'page': page,
                'form': form,
                'investor_form_set': investor_form_set
            }
            return render(request, self.template_name, context)


class FundingRoundListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, "dashboard/funding_round/funding_round_list.html", {'page': page})


class FundingRoundListJson(LoginRequiredMixin, BaseDatatableView):
    model = FundingRound
    # define the columns that will be returned
    columns = ['id', 'investee_organization', 'announced_date_year', 'id']
    order_columns = ['id', 'investee_organization']

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
                escape("{0}".format(item.investee_organization.name)),
                escape(get_formatted_date(item.announced_date_year, item.announced_date_month, item.announced_date_day)),
                escape("{0}".format(str(item.id))),
            ])
        return json_data


class FundingRoundDeleteView(LoginRequiredMixin, DeleteView):
    model = FundingRound
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
