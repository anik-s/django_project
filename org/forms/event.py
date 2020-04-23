from django import forms
from org.models import EventType, Country, City, EventSubCategory, EventCategory, AppearanceType, Person, Event, \
    EventPerson, EventOrganization, Organization
from django.forms import formset_factory
from django.forms import ModelChoiceField
from .common import day_choices, year_choices, month_choices, PersonSelect2Widget, OrganizationSelect2Widget, \
    delete_choices


class PlatformBusinessModelTypeChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class EventTypeChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class CountryChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class CityChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class EventCategoryChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class EventSubCategoryChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class AppearanceChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class EventForm(forms.Form):
    profile_image = forms.ImageField(label="Profile Image", required=False)
    name = forms.CharField(label="Event Name", widget=forms.TextInput(attrs={'class': "form-control",
                                                                             "placeholder": "Event Name"}))
    event_type = EventTypeChoiceField(queryset=EventType.objects.all(), empty_label="-- Select Event Type --",
                                      to_field_name="id", widget=forms.Select(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    start_date_year = forms.ChoiceField(label="Year", required=False, choices=year_choices,
                                        widget=forms.Select(attrs={'class': 'form-control'}))
    start_date_month = forms.ChoiceField(label="Month", required=False, choices=month_choices,
                                         widget=forms.Select(attrs={'class': 'form-control'}))
    start_date_day = forms.ChoiceField(label="Day", required=False, choices=day_choices,
                                       widget=forms.Select(attrs={'class': 'form-control'}))
    end_date_year = forms.ChoiceField(label="Year", required=False, choices=year_choices,
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    end_date_month = forms.ChoiceField(label="Month", required=False, choices=month_choices,
                                       widget=forms.Select(attrs={'class': 'form-control'}))
    end_date_day = forms.ChoiceField(label="Day", required=False, choices=day_choices,
                                     widget=forms.Select(attrs={'class': 'form-control'}))
    event_url = forms.URLField(label="Event URL", required=False, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                                'placeholder': 'Event URL'}))
    registration_url = forms.URLField(label="Registration URL", required=False,
                                      widget=forms.TextInput(attrs={'class': 'form-control',
                                                                    'placeholder': 'Registration URL'}))
    full_description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    venue_address = forms.CharField(label="Venue Address", required=False,
                                    widget=forms.Textarea(attrs={'class': 'form-control'}))
    country = CountryChoiceField(queryset=Country.objects.all(), required=False, empty_label="-- Select Country --",
                                 to_field_name="id", widget=forms.Select(attrs={'class': 'form-control',
                                                                                'id': 'country-select'}))
    city = CityChoiceField(queryset=City.objects.all(), required=False, empty_label="-- Select City --",
                           to_field_name="id", widget=forms.Select(attrs={'class': 'form-control',
                                                                          'id': 'city-select'}))
    category = EventCategoryChoiceField(queryset=EventCategory.objects.all(), required=False,
                                        empty_label="-- Select Category --",
                                        to_field_name="id", widget=forms.Select(attrs={'class': 'form-control',
                                                                                       'id': 'category-select'}))
    sub_category = EventSubCategoryChoiceField(queryset=EventSubCategory.objects.all(), required=False,
                                               empty_label="-- Select Sub Category --",
                                               to_field_name="id", widget=forms.Select(attrs={'class': 'form-control',
                                                                                              'id': 'sub-category-select'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()
        self.fields['sub_category'].queryset = EventSubCategory.objects.none()

        # if 'country' in self.data:
        #     print(self.data.get('country'))
        #     try:
        #         country_id = int(self.data.get('country'))
        #         self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
        #     except (ValueError, TypeError):
        #         pass  # invalid input from the client; ignore and fallback to empty City queryset
        # else:
        #     self.fields['city'].queryset = City.objects.none()

    def clean(self):
        cleaned_data = super().clean()

        # start date validation
        start_date_year = cleaned_data.get('start_date_year')
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

    def save(self):
        data = self.cleaned_data
        event = Event(
            profile_image=data['profile_image'],
            name=data["name"],
            event_type=data["event_type"],
            description=data["description"],
            start_date_day=data["start_date_day"],
            start_date_month=data["start_date_month"],
            start_date_year=data["start_date_year"],
            end_date_day=data["end_date_day"],
            end_date_month=data["end_date_month"],
            end_date_year=data["end_date_year"],
            event_url=data["event_url"],
            registration_url=data["registration_url"],
            full_description=data["full_description"],
            venue_address=data["venue_address"],
            venue_country=data["country"],
            venue_city=data["city"],
            event_category=data["category"],
            event_sub_category=data["sub_category"]
        )
        event.save()
        return event

    def update(self, event):
        data = self.cleaned_data
        event.profile_image = data['profile_image']
        event.name = data["name"]
        event.event_type = data["event_type"]
        event.description = data["description"]
        event.start_date_year = data["start_date_year"]
        event.start_date_month = data["start_date_month"]
        event.start_date_day = data["start_date_day"]
        event.end_date_year = data["end_date_year"]
        event.end_date_month = data["end_date_month"]
        event.end_date_day = data["end_date_day"]
        event.event_url = data["event_url"]
        event.registration_url = data["registration_url"]
        event.full_description = data["full_description"]
        event.venue_country = data["country"]
        event.venue_city = data["city"]
        event.venue_address = data["venue_address"]
        event.event_category = data["category"]
        event.event_sub_category = data["sub_category"]
        event.save()
        return event


participant_types = [('person', 'Person'), ('organization', 'Organization')]


class AppearanceForm(forms.Form):
    p_type = forms.ChoiceField(label="Choose Type", choices=participant_types,
                               widget=forms.RadioSelect(attrs={'class': 'radio-appearance-type'}))
    appearance_type = AppearanceChoiceField(queryset=AppearanceType.objects.all(), required=False,
                                            empty_label="-- Select Appearance Type --",
                                            widget=forms.Select(attrs={'class': 'form-control'}))
    person = ModelChoiceField(label="Persons", queryset=Person.objects.all(),
                              empty_label="Search Person", required=False,
                              widget=PersonSelect2Widget(attrs={'class': 'form-control'}))
    organization = ModelChoiceField(label="Organizations", queryset=Organization.objects.all(),
                                    empty_label="Search Organization", required=False,
                                    widget=OrganizationSelect2Widget(attrs={'class': 'form-control'}))
    deleted = forms.ChoiceField(label="Deleted", required=True, choices=delete_choices, initial='0',
                                widget=forms.Select(attrs={'class': 'form-control deleted'}))

    def clean(self):
        cleaned_data = self.cleaned_data
        p_type = cleaned_data.get("p_type")
        person = cleaned_data.get("person")
        organization = cleaned_data.get("organization")
        deleted = cleaned_data.get("deleted")
        if deleted == '0':
            if p_type == 'person' and person is None:
                msg = "This field is required"
                self.add_error('person', msg)
            elif p_type == 'organization' and organization is None:
                msg = "This field is required"
                self.add_error('organization', msg)

    def save(self, event):
        # data = super().clean()
        cleaned_data = self.cleaned_data
        print(cleaned_data)
        deleted = cleaned_data.get("deleted")
        if deleted == '0':
            if cleaned_data.get('p_type') == 'person':
                person = cleaned_data.get('person')
                event_person = EventPerson(event=event, person=person,
                                           appearance_type=cleaned_data.get('appearance_type'))
                event_person.save()
            elif cleaned_data.get('p_type') == 'organization':
                organization = cleaned_data.get('organization')
                event_org = EventOrganization(event=event, organization=organization,
                                              appearance_type=cleaned_data.get('appearance_type'))
                event_org.save()


AppearanceFormSet = formset_factory(AppearanceForm, min_num=0, validate_min=True)
