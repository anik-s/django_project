from django.shortcuts import render
from django.views import View
from org.models import Organization, Person
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from org.views.helper import get_formatted_date


class PersonListView(View):

    page = 'person'

    def get(self, request, *args, **kwargs):
        return render(request, "frontend/person/persons.html", {'page': self.page})


class PersonListJson(BaseDatatableView):
    model = Person
    columns = ['id', 'first_name', 'type', 'city']
    order_columns = ['name', 'first_name']

    max_display_length = 50

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            location = ""
            city = ""
            if item.city is not None:
                city = item.city.name
            country = ""
            if item.country is not None:
                country = item.country.name
            if country != "" and city != "":
                location = city + ", " + country
            json_data.append([
                escape("{0}".format(str(item.id))),
                escape("{0} {1}".format(item.first_name, item.last_name)),
                escape("{0}".format(item.type)),
                escape("{0}".format(location)),
            ])
        return json_data
