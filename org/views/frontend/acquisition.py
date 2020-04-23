from django.shortcuts import render
from django.views import View
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape

from org.models import Acquisition
from org.views.helper import get_formatted_date


class AcquisitionListView(View):
    page = 'acquisition'

    def get(self, request, *args, **kwargs):
        return render(request, "frontend/acquisition/acquisitions.html", {'page': self.page})


class AcquisitionListJson(BaseDatatableView):
    model = Acquisition
    # define the columns that will be returned
    columns = ['id', 'transaction_name', 'acquiring_organization', 'acquired_organization', 'announced_date_year']
    order_columns = ['id', 'transaction_name']

    def prepare_results(self, qs):
        # prepare list with output column data
        # queryset is already paginated here
        json_data = []
        for item in qs:
            json_data.append([
                escape("{0}".format(str(item.id))),
                escape("{0}".format(item.transaction_name)),

                escape("{0}".format(item.acquired_organization.name)),
                escape("{0}".format(item.acquiring_organization.name)),

                escape(get_formatted_date(item.announced_date_year, item.announced_date_month, item.announced_date_day)),

                # extra
                escape("{0}".format(item.acquired_organization.id)),
                escape("{0}".format(item.acquiring_organization.id))
            ])
        return json_data
