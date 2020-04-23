from django import forms
from django.forms import ChoiceField, ModelChoiceField
from django_select2.forms import ModelSelect2Widget

from org.models import Organization, Acquisition, Currency, AcquisitionType, Disposition, AcquisitionStatus, \
    AcquisitionTerm
from .common import day_choices, month_choices, year_choices, CurrencyChoiceField, OrganizationSelect2Widget


class AcquisitionTypeChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class AcquisitionStatusChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class DispositionChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class AcquisitionTermChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class AcquisitionForm(forms.ModelForm):
    acquiring_organization = ModelChoiceField(label="Acquiring Organization", queryset=Organization.objects.all(),
                                              empty_label="Search Organization",
                                              widget=OrganizationSelect2Widget(attrs={'class': 'form-control'}))
    acquired_organization = ModelChoiceField(label="Acquired Organization", queryset=Organization.objects.all(),
                                             empty_label="Search Organization",
                                             widget=OrganizationSelect2Widget(attrs={'class': 'form-control'}))
    announced_date_year = forms.ChoiceField(label="Year", required=True, choices=year_choices,
                                            widget=forms.Select(attrs={'class': 'form-control'}))

    announced_date_month = forms.ChoiceField(label="Month", required=False, choices=month_choices,
                                             widget=forms.Select(attrs={'class': 'form-control'}))
    announced_date_day = forms.ChoiceField(label="Day", required=False, choices=day_choices,
                                           widget=forms.Select(attrs={'class': 'form-control'}))
    completed_date_year = forms.ChoiceField(label="Year", required=False, choices=year_choices,
                                            widget=forms.Select(attrs={'class': 'form-control'}))

    completed_date_month = forms.ChoiceField(label="Month", required=False, choices=month_choices,
                                             widget=forms.Select(attrs={'class': 'form-control'}))
    completed_date_day = forms.ChoiceField(label="Day", required=False, choices=day_choices,
                                           widget=forms.Select(attrs={'class': 'form-control'}))
    price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    currency = CurrencyChoiceField(queryset=Currency.objects.all(), required=False, empty_label="-- Select Currency --",
                                   to_field_name="id", widget=forms.Select(attrs={'class': 'form-control'}))
    acquisition_type = AcquisitionTypeChoiceField(queryset=AcquisitionType.objects.all(), required=False,
                                                  empty_label="-- Select Acquisition Type --", to_field_name="id",
                                                  widget=forms.Select(attrs={'class': 'form-control', }))
    acquisition_status = AcquisitionStatusChoiceField(queryset=AcquisitionStatus.objects.all(), required=False,
                                                      empty_label="-- Select Acquisition Status --", to_field_name="id",
                                                      widget=forms.Select(attrs={'class': 'form-control'}))
    disposition = DispositionChoiceField(queryset=Disposition.objects.all(), required=False,
                                         empty_label="-- Select Disposition --", to_field_name="id",
                                         widget=forms.Select(attrs={'class': 'form-control'}))
    acquisition_term = AcquisitionTermChoiceField(queryset=AcquisitionTerm.objects.all(), required=False,
                                                  empty_label="-- Select Acquisition Term --", to_field_name="id",
                                                  widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Acquisition
        fields = [
            'acquiring_organization',
            'acquired_organization',
            'announced_date_year',
            'announced_date_month',
            'announced_date_day',
            'completed_date_year',
            'completed_date_month',
            'completed_date_day',
            'price',
            'currency',
            'acquisition_type',
            'acquisition_status',
            'disposition',
            'acquisition_term'
        ]

    # def clean_announced_date_month(self):
    #     data = self.cleaned_data['announced_date_month']
    #     if data == "":
    #         data = None
    #     return data
    #
    # def clean_announced_date_day(self):
    #     data = self.cleaned_data['announced_date_day']
    #     if data == "":
    #         data = None
    #     return data
    #
    # def clean_completed_date_year(self):
    #     data = self.cleaned_data['completed_date_year']
    #     if data == "":
    #         data = None
    #     return data
    #
    # def clean_completed_date_month(self):
    #     data = self.cleaned_data['completed_date_month']
    #     if data == "":
    #         data = None
    #     return data
    #
    # def clean_completed_date_day(self):
    #     data = self.cleaned_data['completed_date_day']
    #     if data == "":
    #         data = None
    #     return data

    # def __init__(self, *args, **kwargs):
    #     super(AcquisitionForm, self).__init__(*args, **kwargs)
    #     self.fields['acquiring_organization'].widget = OrganizationSelect2Widget()
    #     self.fields['acquiring_organization'].label = "nfn"
    #     self.fields['acquiring_organization'].widget.attrs.update({
    #         'class': 'form-control'
    # })
