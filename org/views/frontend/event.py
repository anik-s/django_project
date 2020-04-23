from django.shortcuts import render
from django.views import View
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from org.models import Event
from org.views.helper import get_formatted_date

page = 'event'


class EventListView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "frontend/event/events.html", {'page': page})


class EventListJson(BaseDatatableView):
    model = Event
    # define the columns that will be returned
    columns = ['id', 'name', 'start_date_year', 'end_date_year', 'venue_city']
    order_columns = ['id', 'name', 'venue_city']

    max_display_length = 50

    def prepare_results(self, qs):
        # prepare list with output column data
        # queryset is already paginated here
        json_data = []
        for item in qs:
            location = ""
            city = ""
            if item.venue_city is not None:
                city = item.venue_city.name
            country = ""
            if item.venue_country is not None:
                country = item.venue_country.name
            if country != "" and city != "":
                location = city + ", " + country

            json_data.append([
                escape("{0}".format(str(item.id))),
                escape("{0}".format(item.name)),
                escape(get_formatted_date(item.start_date_year, item.start_date_month, item.start_date_day)),
                escape(get_formatted_date(item.end_date_year, item.end_date_month, item.end_date_day)),
                escape("{0}".format(location)),
            ])
        return json_data