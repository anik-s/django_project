from django import forms
from django.forms import ModelChoiceField, formset_factory

from org.forms.common import year_choices, month_choices, day_choices, OrganizationSelect2Widget, delete_choices
from org.forms.event import CountryChoiceField, CityChoiceField, PlatformBusinessModelTypeChoiceField
from org.forms.person import InvestorStageChoiceField
from org.forms.platform import get_org_category_choices
from org.models import City, OrganizationType, CompanyType, InvestorType, InvestmentStage, Country, \
    PlatformBusinessModelType, Organization, StockExchange, OrganizationRelation, OrgSubOrganization, OrganizationCategory

no_of_employees_choices = (
    ("", "-- Select no of Employees --"),
    ("1-10", "1-10"),
    ("11-50", "11-50"),
    ("51-100", "51-100"),
)

organization_type_choices = (
    ("Company", "Company"),
    ("Investment Firm", "Investment Firm")
)


class OrganizationTypeChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class CompanyTypeChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class InvestorTypeChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class StockExchangeChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class OrganizationRelationChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class OrganizationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['industry_categories'].choices = get_org_category_choices()
        if 'country' in self.data:
            print(self.data.get('country'))
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        else:
            self.fields['city'].queryset = City.objects.none()

    profile_image = forms.ImageField(label="Profile Image", required=False)
    organization_type = forms.ChoiceField(label="Choose Type", choices=organization_type_choices,
                                          widget=forms.RadioSelect(attrs={'class': 'radio-type'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    aka = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    legal_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    founded_date_year = forms.ChoiceField(label="Year", required=False, choices=year_choices,
                                          widget=forms.Select(attrs={'class': 'form-control'}))
    founded_date_month = forms.ChoiceField(label="Month", required=False, choices=month_choices,
                                           widget=forms.Select(attrs={'class': 'form-control'}))
    founded_date_day = forms.ChoiceField(label="Day", required=False, choices=day_choices,
                                         widget=forms.Select(attrs={'class': 'form-control'}))
    closed_date_year = forms.ChoiceField(label="Year", required=False, choices=year_choices,
                                         widget=forms.Select(attrs={'class': 'form-control'}))
    closed_date_month = forms.ChoiceField(label="Month", required=False, choices=month_choices,
                                          widget=forms.Select(attrs={'class': 'form-control'}))
    closed_date_day = forms.ChoiceField(label="Day", required=False, choices=day_choices,
                                        widget=forms.Select(attrs={'class': 'form-control'}))
    number_of_employees = forms.ChoiceField(label="No of Employees", required=False, choices=no_of_employees_choices,
                                            widget=forms.Select(attrs={'class': 'form-control'}))
    company_type = CompanyTypeChoiceField(queryset=CompanyType.objects.all(),
                                          label='Company Type (in case of Company)', required=False,
                                          empty_label="-- Select Company Type --",
                                          to_field_name="id", widget=forms.Select(attrs={'class': 'form-control'}))
    investor_type = InvestorTypeChoiceField(queryset=InvestorType.objects.all(),
                                            label='Investor Type (in case of Investment Firm)', required=False,
                                            empty_label="-- Select Investor Type --",
                                            to_field_name="id", widget=forms.Select(attrs={'class': 'form-control'}))
    investment_stage = InvestorStageChoiceField(queryset=InvestmentStage.objects.all(), required=False,
                                                label='Investment Stage (in case of Investment Firm)',
                                                empty_label="-- Select Investor Type --",
                                                to_field_name="id",
                                                widget=forms.Select(attrs={'class': 'form-control'}))
    website = forms.URLField(label="Website", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    facebook = forms.URLField(label="Facebook", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    linkedin = forms.URLField(label="LinkedIn", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    twitter = forms.URLField(label="Twitter", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    contact_email = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    full_description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    country = CountryChoiceField(queryset=Country.objects.all(), required=False, empty_label="-- Select Country --",
                                 to_field_name="id", widget=forms.Select(attrs={'class': 'form-control',
                                                                                'id': 'country-select'}))
    city = CityChoiceField(queryset=City.objects.all(), required=False, empty_label="-- Select City --",
                           to_field_name="id",
                           widget=forms.Select(attrs={'class': 'form-control', 'id': 'city-select'}))
    industry_categories = forms.MultipleChoiceField(choices=(), required=False)
    platform_business_mode_type = PlatformBusinessModelTypeChoiceField(
        queryset=PlatformBusinessModelType.objects.all(),
        empty_label="-- Select Platform Model Type --",
        to_field_name="id", required=False,
        widget=forms.Select(attrs={'class': 'form-control'}))
    stock_symbol = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    stock_exchange = StockExchangeChoiceField(queryset=StockExchange.objects.all(), required=False,
                                              empty_label="-- Select Stock Exchange --",
                                              to_field_name="id", widget=forms.Select(attrs={'class': 'form-control'}))
    ipo_date_year = forms.ChoiceField(label="Year", required=False, choices=year_choices,
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    ipo_date_month = forms.ChoiceField(label="Month", required=False, choices=month_choices,
                                       widget=forms.Select(attrs={'class': 'form-control'}))
    ipo_date_day = forms.ChoiceField(label="Day", required=False, choices=day_choices,
                                     widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Organization
        fields = [
            'profile_image',
            'organization_type',
            'name',
            'description',
            'aka',
            'legal_name',
            'founded_date_year',
            'founded_date_month',
            'founded_date_day',
            'closed_date_year',
            'closed_date_month',
            'closed_date_day',
            'number_of_employees',
            'company_type',
            'investor_type',
            'investment_stage',
            'website',
            'facebook',
            'linkedin',
            'twitter',
            'contact_email',
            'phone_number',
            'full_description',
            'country',
            'city',
            'platform_business_mode_type',
            'stock_symbol',
            'stock_exchange',
            'ipo_date_year',
            'ipo_date_month',
            'ipo_date_day'
        ]


class SubOrganizationForm(forms.Form):
    organization = ModelChoiceField(label="Sub Organization", queryset=Organization.objects.all(),
                                    empty_label="Search Organization", required=False,
                                    widget=OrganizationSelect2Widget(attrs={'class': 'form-control'}))
    relation = OrganizationRelationChoiceField(queryset=OrganizationRelation.objects.all(), required=False,
                                               empty_label="-- Select Relation --", label='Relationship with Parent',
                                               to_field_name="id", widget=forms.Select(attrs={'class': 'form-control'}))
    deleted = forms.ChoiceField(label="Deleted", required=True, choices=delete_choices, initial='0',
                                widget=forms.Select(attrs={'class': 'form-control deleted'}))

    def clean(self):
        cleaned_data = self.cleaned_data
        organization = cleaned_data.get("organization")
        relation = cleaned_data.get("relation")
        deleted = cleaned_data.get("deleted")
        if deleted == '0':
            if organization is not None and relation is None:
                msg = "This field is required"
                self.add_error('relation', msg)
            if organization is None and relation is not None:
                msg = "This field is required"
                self.add_error('organization', msg)

    def save(self, org):
        cleaned_data = self.cleaned_data
        organization = cleaned_data.get("organization")
        relation = cleaned_data.get("relation")
        deleted = cleaned_data.get("deleted")
        if deleted == '0':
            OrgSubOrganization(organization=org, sub_organization=organization, relation=relation).save()


SubOrganizationFormSet = formset_factory(SubOrganizationForm, min_num=0, validate_min=True)
