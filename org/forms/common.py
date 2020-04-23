from django.forms import ModelChoiceField
from django_select2.forms import ModelSelect2MultipleWidget, ModelSelect2Widget

from org.models import Person, Organization, Platform, FundingRound, Acquisition, Event

delete_choices = (
    ("0", "0"),
    ("1", "1")
)


year_choices = (
    ("", "-- Select Year --"),
    ("2020", "2020"),
    ("2019", "2019"),
    ("2018", "2018"),
    ("2017", "2017"),
    ("2016", "2016"),
)

month_choices = (
    ("", "-- Select Month --"),
    ("January", "January"),
    ("February", "February"),
    ("March", "March"),
    ("April", "April"),
    ("May", "May"),
    ("June", "June"),
    ("July", "July"),
    ("August", "August"),
    ("September", "September"),
    ("October", "October"),
    ("November", "November"),
    ("December", "December"),
)

day_choices = (
    ("", "-- Select Date --"),
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
    ("7", "7"),
    ("8", "8"),
    ("9", "9"),
    ("10", "10"),
    ("11", "11"),
    ("12", "12"),
    ("13", "13"),
    ("14", "14"),
    ("15", "15"),
    ("16", "16"),
    ("17", "17"),
    ("18", "18"),
    ("19", "19"),
    ("20", "20"),
    ("21", "21"),
    ("22", "22"),
    ("23", "23"),
    ("24", "24"),
    ("25", "25"),
    ("26", "26"),
    ("27", "27"),
    ("28", "28"),
    ("29", "29"),
    ("30", "30"),
    ("31", "31"),
)


class PersonSelect2MultipleWidget(ModelSelect2MultipleWidget):
    search_fields = [
        'first_name__icontains',
    ]
    model = Person
    queryset = Person.objects.all()

    def label_from_instance(self, obj):
        return str(obj.first_name)


class OrganizationSelect2MultipleWidget(ModelSelect2MultipleWidget):
    search_fields = [
        'name__icontains',
    ]
    model = Organization
    queryset = Organization.objects.all()

    def label_from_instance(self, obj):
        return str(obj.name)


class PersonSelect2Widget(ModelSelect2Widget):
    search_fields = [
        'first_name__icontains',
    ]
    model = Person
    queryset = Person.objects.all()

    def label_from_instance(self, obj):
        return str(obj.first_name)


class OrganizationSelect2Widget(ModelSelect2Widget):
    search_fields = [
        'name__icontains',
    ]
    model = Organization
    queryset = Organization.objects.all()

    def label_from_instance(self, obj):
        return str(obj.name)


class PlatformSelect2Widget(ModelSelect2Widget):
    search_fields = [
        'name__icontains',
    ]
    model = Platform
    queryset = Platform.objects.all()

    def label_from_instance(self, obj):
        return str(obj.name)


class FundingSelect2Widget(ModelSelect2Widget):
    search_fields = [
        'name__icontains',
    ]
    model = FundingRound
    queryset = FundingRound.objects.all()

    def label_from_instance(self, obj):
        return str(obj.name)


class AcquisitionSelect2Widget(ModelSelect2Widget):
    search_fields = [
        'name__icontains',
    ]
    model = Acquisition
    queryset = Acquisition.objects.all()

    def label_from_instance(self, obj):
        return str(obj.name)


class EventSelect2Widget(ModelSelect2Widget):
    search_fields = [
        'name__icontains',
    ]
    model = Event
    queryset = Event.objects.all()

    def label_from_instance(self, obj):
        return str(obj.name)


class CurrencyChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name