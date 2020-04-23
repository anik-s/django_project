from django import forms
from django.forms import ModelChoiceField

from org.forms.common import year_choices, month_choices, day_choices, OrganizationSelect2Widget
from org.forms.event import PlatformBusinessModelTypeChoiceField
from org.models import Organization, Platform, OrganizationCategory, OrganizationSubCategory, PlatformBusinessModelType


def get_org_category_choices():
    d = []
    cats = OrganizationCategory.objects.all()
    for c in cats:
        c_name = c.name
        s_cats = OrganizationSubCategory.objects.filter(category=c)
        s_cat_list = []
        for sc in s_cats:
            s_cat_list.append((str(sc.id), sc.name))
        if len(s_cat_list) > 0:
            d.append((c_name, tuple(s_cat_list)))
    return d


class PlatformForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['industry_categories'].choices = get_org_category_choices()

    profile_image = forms.ImageField(label="Profile Image", required=False,
                                     widget=forms.FileInput(attrs={'class': 'form-control'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
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
    website = forms.URLField(label="Website", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    facebook = forms.URLField(label="Facebook", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    linkedin = forms.URLField(label="LinkedIn", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    twitter = forms.URLField(label="Twitter", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    contact_email = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    full_description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    owned_by_organization = ModelChoiceField(required=False, label="Find an Organization",
                                             queryset=Organization.objects.all(),
                                             empty_label="Search Organization",
                                             widget=OrganizationSelect2Widget(attrs={'class': 'form-control'}))
    producers = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    consumers = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    partners = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    transactions = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    value = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    network_effects = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    industry_categories = forms.MultipleChoiceField(choices=(), required=False)
    platform_business_model_type = PlatformBusinessModelTypeChoiceField(
        queryset=PlatformBusinessModelType.objects.all(),
        empty_label="-- Select Platform Model Type --",
        to_field_name="id", required=False,
        widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Platform
        fields = [
            'industry_categories',
            'platform_business_model_type',
            'profile_image',
            'name',
            'description',
            'founded_date_year',
            'founded_date_month',
            'founded_date_day',
            'closed_date_year',
            'closed_date_month',
            'closed_date_day',
            'website',
            'facebook',
            'linkedin',
            'twitter',
            'contact_email',
            'phone_number',
            'full_description',
            'owned_by_organization',
            'producers',
            'consumers',
            'partners',
            'transactions',
            'value',
            'network_effects'
        ]
