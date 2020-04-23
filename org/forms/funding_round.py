from django import forms
from django.forms import ModelChoiceField, formset_factory

from org.forms.common import OrganizationSelect2Widget, year_choices, month_choices, day_choices, CurrencyChoiceField, \
    PersonSelect2Widget, delete_choices
from org.models import FundingRound, Organization, FundingType, Currency, Person, FundingRoundInvestor, \
    FundingRoundInvestorOrganization


class FundingTypeChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class FundingRoundForm(forms.ModelForm):
    investee_organization = ModelChoiceField(label="Company*", queryset=Organization.objects.all(),
                                             empty_label="Search Organization",
                                             widget=OrganizationSelect2Widget(attrs={'class': 'form-control'}))
    funding_type = FundingTypeChoiceField(queryset=FundingType.objects.all(), label='Funding Type*', empty_label="-- Select Funding Type --",
                                          to_field_name="id", widget=forms.Select(attrs={'class': 'form-control'}))

    announced_date_year = forms.ChoiceField(label="Year", choices=year_choices,
                                            widget=forms.Select(attrs={'class': 'form-control'}))
    announced_date_month = forms.ChoiceField(label="Month", required=False, choices=month_choices,
                                             widget=forms.Select(attrs={'class': 'form-control'}))
    announced_date_day = forms.ChoiceField(label="Day", required=False, choices=day_choices,
                                           widget=forms.Select(attrs={'class': 'form-control'}))
    closed_date_year = forms.ChoiceField(label="Year", required=False, choices=year_choices,
                                         widget=forms.Select(attrs={'class': 'form-control'}))
    closed_date_month = forms.ChoiceField(label="Month", required=False, choices=month_choices,
                                          widget=forms.Select(attrs={'class': 'form-control'}))
    closed_date_day = forms.ChoiceField(label="Day", required=False, choices=day_choices,
                                        widget=forms.Select(attrs={'class': 'form-control'}))
    money_raised = forms.DecimalField(label="Money Raised", required=False,
                                      widget=forms.TextInput(attrs={'class': "form-control",
                                                                    "placeholder": "Money Raised"}))
    money_raised_currency = CurrencyChoiceField(queryset=Currency.objects.all(), required=False,
                                                empty_label="-- Select Currency --",
                                                to_field_name="id",
                                                widget=forms.Select(attrs={'class': 'form-control'}))
    target_funding = forms.DecimalField(label="Target Funding", required=False, widget=forms.TextInput(
        attrs={'class': "form-control", "placeholder": "Target Funding"}))
    target_funding_currency = CurrencyChoiceField(queryset=Currency.objects.all(), empty_label="-- Select Currency --",
                                                  to_field_name="id", required=False,
                                                  widget=forms.Select(attrs={'class': 'form-control'}))
    pre_money_valuation = forms.DecimalField(label="Pre-Money Valuation", required=False,
                                             widget=forms.TextInput(attrs={'class': "form-control",
                                                                           "placeholder": "Pre Money Valuation"}))
    pre_money_valuation_currency = CurrencyChoiceField(queryset=Currency.objects.all(),
                                                       empty_label="-- Select Currency --",
                                                       to_field_name="id", required=False,
                                                       widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = FundingRound
        fields = [
            'investee_organization',
            'funding_type',
            'announced_date_year',
            'announced_date_month',
            'announced_date_day',
            'closed_date_year',
            'closed_date_month',
            'closed_date_day',
            'money_raised',
            'money_raised_currency',
            'target_funding',
            'target_funding_currency',
            'pre_money_valuation',
            'pre_money_valuation_currency'
        ]


investor_types = [('person', 'Individual Investor'), ('organization', 'Investment Firm')]
lead_investor_choices = (("", "-- Select Lead Investor --"),
                         ("True", "True"),
                         ("False", "False"))


class InvestorForm(forms.Form):
    investor_type = forms.ChoiceField(label="Choose Type", choices=investor_types,
                                      widget=forms.RadioSelect(attrs={'class': 'radio-investor-type'}))
    person = ModelChoiceField(label="Person", queryset=Person.objects.all(),
                              empty_label="Search Person", required=False,
                              widget=PersonSelect2Widget(attrs={'class': 'form-control'}))
    organization = ModelChoiceField(label="Organization", queryset=Organization.objects.all(),
                                    empty_label="Search Organization", required=False,
                                    widget=OrganizationSelect2Widget(attrs={'class': 'form-control'}))
    lead_investor = forms.ChoiceField(label="Lead Investor", choices=lead_investor_choices,
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    money_raised = forms.DecimalField(label="Money Raised", required=False,
                                      widget=forms.TextInput(attrs={'class': "form-control",
                                                                    "placeholder": "Money Raised"}))
    money_raised_currency = CurrencyChoiceField(queryset=Currency.objects.all(), required=False,
                                                empty_label="-- Select Currency --",
                                                to_field_name="id",
                                                widget=forms.Select(attrs={'class': 'form-control'}))
    deleted = forms.ChoiceField(label="Deleted", required=True, choices=delete_choices, initial='0',
                                widget=forms.Select(attrs={'class': 'form-control deleted'}))

    def clean(self):
        cleaned_data = self.cleaned_data
        investor_type = cleaned_data.get("investor_type")
        person = cleaned_data.get("person")
        organization = cleaned_data.get("organization")
        lead_investor = cleaned_data.get("lead_investor")
        money_raised = cleaned_data.get("money_raised")
        money_raised_currency = cleaned_data.get("money_raised_currency")
        deleted = cleaned_data.get("deleted")
        if deleted == '0':
            if investor_type == 'person' and person is None:
                msg = "This field is required"
                self.add_error('person', msg)
            elif investor_type == 'organization' and organization is None:
                msg = "This field is required 23"
                self.add_error('organization', msg)

    def save(self, funding_round):
        cleaned_data = self.cleaned_data
        investor_type = cleaned_data.get("investor_type")
        person = cleaned_data.get("person")
        organization = cleaned_data.get("organization")
        lead_investor = cleaned_data.get("lead_investor")
        money_raised = cleaned_data.get("money_raised")
        money_raised_currency = cleaned_data.get("money_raised_currency")
        deleted = cleaned_data.get("deleted")
        if deleted == '0':
            if investor_type == 'person':
                FundingRoundInvestor(funding_round=funding_round,
                                     person=person,
                                     lead_investor=lead_investor,
                                     money_raised=money_raised,
                                     money_raised_currency=money_raised_currency).save()
            elif investor_type == 'organization':
                FundingRoundInvestorOrganization(funding_round=funding_round, investor_organization=organization,
                                                 lead_investor=lead_investor,
                                                 money_raised=money_raised,
                                                 money_raised_currency=money_raised_currency).save()


InvestorFormSet = formset_factory(InvestorForm, min_num=0, validate_min=True)
