from django.shortcuts import render
from django.views import View
from org.models import Organization
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from org.views.helper import get_formatted_date


class OrganizationListView(View):

    page = 'organization'

    def get(self, request, *args, **kwargs):
        return render(request, "frontend/organization/organizations.html", {'page': self.page})


class OrganizationListJson(BaseDatatableView):
    model = Organization
    columns = ['id', 'name', 'description', 'description', 'city', 'founded_date_year']
    order_columns = ['name', 'description']

    max_display_length = 50

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            o_cats = []
            for c in item.organizationhascategory_set.all():
                o_cats.append(c.category.name)
            city = ""
            if item.city is not None:
                city = item.city.name
            json_data.append([
                escape("{0}".format(str(item.id))),
                escape("{0}".format(item.name)),
                escape("{0}".format(item.description)),
                escape("{0}".format(', '.join(o_cats))),
                escape("{0}".format(city)),
                escape("{0}".format(get_formatted_date(item.founded_date_year, item.founded_date_month,
                                                       item.founded_date_day))),
            ])
        return json_data
