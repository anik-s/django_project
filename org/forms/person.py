from django import forms
from django.forms import ModelChoiceField, formset_factory, ModelMultipleChoiceField
from org.forms.common import year_choices, month_choices, day_choices, delete_choices, OrganizationSelect2MultipleWidget
from org.forms.event import CountryChoiceField, CityChoiceField
from org.models import Person, Gender, InvestorStage, Country, City, PersonType, JobPosition, PersonJob, Organization


class GenderChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class PersonTypeChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class InvestorStageChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


person_type_choices = (
    ("Person", "Person"),
    ("Individual Investor", "Individual Investor")
)


class PersonForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['city'].queryset = City.objects.none()
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
    type = forms.ChoiceField(label="Choose Type", choices=person_type_choices,
                                          widget=forms.RadioSelect(attrs={'class': 'radio-type'}))
    first_name = forms.CharField(label='First Name*', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name*', widget=forms.TextInput(attrs={'class': 'form-control'}))
    gender = GenderChoiceField(queryset=Gender.objects.all(), required=False, empty_label="-- Select Gender Type --",
                               to_field_name="id", widget=forms.Select(attrs={'class': 'form-control'}))

    aka = forms.CharField(label='Also Known As', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    investor_stage = InvestorStageChoiceField(queryset=InvestorStage.objects.all(), required=False,
                                              empty_label="-- Select Investor Stage --",
                                              to_field_name="id", widget=forms.Select(attrs={'class': 'form-control'}))
    website = forms.URLField(label="Website URL", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    facebook = forms.URLField(label="Facebook URL", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    linkedin = forms.URLField(label="Linkedin URL", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    twitter = forms.URLField(label="Twitter URL", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    biography = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    country = CountryChoiceField(queryset=Country.objects.all(), required=False, empty_label="-- Select Country --",
                                 to_field_name="id", widget=forms.Select(attrs={'class': 'form-control',
                                                                                'id': 'country-select'}))
    city = CityChoiceField(queryset=City.objects.all(), required=False, empty_label="-- Select City --",
                           to_field_name="id",
                           widget=forms.Select(attrs={'class': 'form-control', 'id': 'city-select'}))
    founded_organizations = ModelMultipleChoiceField(label="Find a Company to add", queryset=Organization.objects.all(),
                                                     required=False,
                                                     widget=OrganizationSelect2MultipleWidget(
                                                         attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        person_type = cleaned_data.get("type")
        investor_stage = cleaned_data.get("investor_stage")
        if person_type == "Individual Investor" and investor_stage is None:
            self.add_error('investor_stage', 'Investor Stage cannot be empty when person type is Individual Investor')

    class Meta:
        model = Person
        fields = [
            'profile_image',
            'type',
            'first_name',
            'last_name',
            'gender',
            'aka',
            'investor_stage',
            'website',
            'facebook',
            'linkedin',
            'twitter',
            'biography',
            'country',
            'city',
            'founded_organizations'
        ]


class JobPositionChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class PersonJobForm(forms.Form):
    profile_image = forms.ImageField(label="Profile Image", required=False)
    position = JobPositionChoiceField(queryset=JobPosition.objects.all(), required=True,
                                      empty_label="-- Select Job Position --",
                                      to_field_name="id", widget=forms.Select(attrs={'class': 'form-control'}))
    title = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    start_date_year = forms.ChoiceField(label="Year", choices=year_choices,
                                        widget=forms.Select(attrs={'class': 'form-control'}))
    start_date_month = forms.ChoiceField(label="Month", required=False, choices=month_choices,
                                         widget=forms.Select(attrs={'class': 'form-control'}))
    start_date_day = forms.ChoiceField(label="Day", required=False, choices=day_choices,
                                       widget=forms.Select(attrs={'class': 'form-control'}))
    has_end_date = forms.BooleanField(label="End Date", required=False,
                                      widget=forms.CheckboxInput(attrs={'class': 'a'}))
    end_date_year = forms.ChoiceField(label="Year", required=False, choices=year_choices,
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    end_date_month = forms.ChoiceField(label="Month", required=False, choices=month_choices,
                                       widget=forms.Select(attrs={'class': 'form-control'}))
    end_date_day = forms.ChoiceField(label="Day", required=False, choices=day_choices,
                                     widget=forms.Select(attrs={'class': 'form-control'}))
    deleted = forms.ChoiceField(label="Deleted", required=True, choices=delete_choices, initial='0',
                                widget=forms.Select(attrs={'class': 'form-control deleted'}))

    def clean(self):
        cleaned_data = self.cleaned_data
        print("+++++++++++++++++++++++++++")
        cleaned_data = super().clean()
        position = cleaned_data.get("position")
        title = cleaned_data.get("title")
        has_end_date = cleaned_data.get('has_end_date')
        deleted = cleaned_data.get("deleted")
        if deleted == '0':

            if position is None:
                self.add_error('position', 'This field is required')
            if title == "":
                self.add_error('title', 'This field is required')

            # start date validation
            start_date_year = cleaned_data.get('start_date_year')
            print("start_date_year")
            print(start_date_year)
            start_date_month = cleaned_data.get('start_date_month')
            start_date_day = cleaned_data.get('start_date_day')
            if start_date_month != "" and start_date_year == "":
                self.add_error('start_date_year', 'Year cannot be empty when month is selected')
            else:
                if start_date_day != "" and start_date_year == "":
                    self.add_error('start_date_year', 'Year cannot be empty when day is selected')
                if start_date_day != "" and start_date_month == "":
                    self.add_error('start_date_month', 'Month cannot be empty when day is selected')

            # end date validation
            if has_end_date:
                end_date_year = cleaned_data.get('end_date_year')
                end_date_month = cleaned_data.get('end_date_month')
                end_date_day = cleaned_data.get('end_date_day')
                if end_date_month != "" and end_date_year == "":
                    self.add_error('end_date_year', 'Year cannot be empty when month is selected')
                else:
                    if end_date_day != "" and end_date_year == "":
                        self.add_error('end_date_year', 'Year cannot be empty when day is selected')
                    if end_date_day != "" and end_date_month == "":
                        self.add_error('end_date_month', 'Month cannot be empty when day is selected')

    def save(self, person):
        cleaned_data = super().clean()
        position = cleaned_data.get("position")
        title = cleaned_data.get("title")
        start_date_year = cleaned_data.get("start_date_year")
        start_date_month = cleaned_data.get("start_date_month")
        start_date_day = cleaned_data.get("start_date_day")
        has_end_date = cleaned_data.get("has_end_date")
        end_date_year = cleaned_data.get("end_date_year")
        end_date_month = cleaned_data.get("end_date_month")
        end_date_day = cleaned_data.get("end_date_day")
        deleted = cleaned_data.get("deleted")

        if deleted == '0':
            person_job = PersonJob(person=person, position=position, title=title, start_date_year=start_date_year,
                                   start_date_month=start_date_month, start_date_day=start_date_day,
                                   has_end_date=has_end_date, end_date_year=end_date_year,
                                   end_date_month=end_date_month, end_date_day=end_date_day)
            person_job.save()


PersonJobFormSet = formset_factory(PersonJobForm, min_num=0, validate_min=True)
