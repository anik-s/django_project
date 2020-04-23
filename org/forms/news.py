from django import forms
from django.forms import ModelChoiceField, formset_factory

from org.models import News, Person, Organization, Platform, FundingRound, Acquisition, Event, PersonNews, \
    OrganizationNews, FundingNews, PlatformNews, AcquisitionNews, EventNews
from .common import day_choices, year_choices, month_choices, delete_choices, PersonSelect2Widget, \
    OrganizationSelect2Widget, \
    PlatformSelect2Widget, FundingSelect2Widget, AcquisitionSelect2Widget, EventSelect2Widget


class NewsForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    url = forms.URLField(label="URL", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_year = forms.ChoiceField(label="Year", required=False, choices=year_choices,
                                        widget=forms.Select(attrs={'class': 'form-control'}))
    date_month = forms.ChoiceField(label="Month", required=False, choices=month_choices,
                                         widget=forms.Select(attrs={'class': 'form-control'}))
    date_day = forms.ChoiceField(label="Day", required=False, choices=day_choices,
                                       widget=forms.Select(attrs={'class': 'form-control'}))
    publisher = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    thumbnail_url = forms.URLField(label="Thumbnail URL", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = News
        fields = [
            'title',
            'url',
            'date_year',
            'date_month',
            'date_day',
            'publisher',
            'thumbnail_url'
        ]

    def clean(self):
        cleaned_data = super().clean()

        # date validation
        date_year = cleaned_data.get('date_year')
        date_month = cleaned_data.get('date_month')
        date_day = cleaned_data.get('date_day')
        if date_month != "" and date_year == "":
            self.add_error('date_year', 'Year cannot be empty when month is selected')
        else:
            if date_day != "" and date_year == "":
                self.add_error('date_year', 'Year cannot be empty when day is selected')
            if date_day != "" and date_month == "":
                self.add_error('date_month', 'Month cannot be empty when day is selected')


mention_types = [('person', 'Person'), ('organization', 'Organization'), ('platform', 'Platform'),
                 ('funding_round', 'Funding'), ('acquisition', 'Acquisition'), ('event', 'Event')]


class NewsMentionForm(forms.Form):
    mention_type = forms.ChoiceField(label="Choose Type", choices=mention_types,
                                     widget=forms.RadioSelect(attrs={'class': 'radio-mention-type'}))
    person = ModelChoiceField(label="Person", queryset=Person.objects.all(),
                              empty_label="Search Person", required=False,
                              widget=PersonSelect2Widget(attrs={'class': 'form-control'}))
    organization = ModelChoiceField(label="Organization", queryset=Organization.objects.all(),
                                    empty_label="Search Organization", required=False,
                                    widget=OrganizationSelect2Widget(attrs={'class': 'form-control'}))
    platform = ModelChoiceField(label="Platform", queryset=Platform.objects.all(),
                                empty_label="Search Platform", required=False,
                                widget=PlatformSelect2Widget(attrs={'class': 'form-control'}))
    funding = ModelChoiceField(label="Funding", queryset=FundingRound.objects.all(),
                               empty_label="Search Funding", required=False,
                               widget=FundingSelect2Widget(attrs={'class': 'form-control'}))
    acquisition = ModelChoiceField(label="Acquisition", queryset=Acquisition.objects.all(),
                                   empty_label="Search Acquisition", required=False,
                                   widget=AcquisitionSelect2Widget(attrs={'class': 'form-control'}))
    event = ModelChoiceField(label="Event", queryset=Event.objects.all(),
                             empty_label="Search Event", required=False,
                             widget=EventSelect2Widget(attrs={'class': 'form-control'}))
    deleted = forms.ChoiceField(label="Deleted", required=True, choices=delete_choices, initial='0',
                                widget=forms.Select(attrs={'class': 'form-control deleted'}))

    def clean(self):
        cleaned_data = self.cleaned_data
        mention_type = cleaned_data.get("mention_type")
        person = cleaned_data.get("person")
        organization = cleaned_data.get("organization")
        funding = cleaned_data.get("funding_round")
        platform = cleaned_data.get("platform")
        acquisition = cleaned_data.get("acquisition")
        event = cleaned_data.get("event")
        deleted = cleaned_data.get("deleted")

        if deleted == '0':
            if mention_type == 'person' and person is None:
                msg = "This field is required"
                self.add_error('person', msg)
            elif mention_type == 'organization' and organization is None:
                msg = "This field is required"
                self.add_error('organization', msg)
            elif mention_type == 'funding_round' and funding is None:
                msg = "This field is required"
                self.add_error('funding', msg)
            elif mention_type == 'platform' and platform is None:
                msg = "This field is required"
                self.add_error('platform', msg)
            elif mention_type == 'acquisition' and acquisition is None:
                msg = "This field is required"
                self.add_error('acquisition', msg)
            elif mention_type == 'event' and event is None:
                msg = "This field is required"
                self.add_error('event', msg)

    def save(self, news):
        cleaned_data = self.cleaned_data
        print(cleaned_data)
        deleted = cleaned_data.get("deleted")
        if deleted == '0':
            if cleaned_data.get('mention_type') == 'person':
                person_news = PersonNews(person=cleaned_data.get("person"), news=news)
                person_news.save()
            elif cleaned_data.get('mention_type') == 'organization':
                o_news = OrganizationNews(organization=cleaned_data.get("organization"), news=news)
                o_news.save()
            elif cleaned_data.get('mention_type') == 'funding_round':
                f_news = FundingNews(funding=cleaned_data.get("funding_round"), news=news)
                f_news.save()
            elif cleaned_data.get('mention_type') == 'platform':
                p_news = PlatformNews(platform=cleaned_data.get("platform"), news=news)
                p_news.save()
            elif cleaned_data.get('mention_type') == 'acquisition':
                p_news = AcquisitionNews(acquisition=cleaned_data.get("acquisition"), news=news)
                p_news.save()
            elif cleaned_data.get('mention_type') == 'event':
                p_news = EventNews(event=cleaned_data.get("event"), news=news)
                p_news.save()


MentionFormSet = formset_factory(NewsMentionForm, min_num=0, validate_min=True)
