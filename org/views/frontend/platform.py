from django.shortcuts import render
from django.views import View
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from org.models import Platform
from org.views.helper import get_formatted_date


class PlatformListView(View):

    page = 'platform'

    def get(self, request, *args, **kwargs):
        return render(request, "frontend/platform/platforms.html", {'page': self.page})


class PlatformListJson(BaseDatatableView):
    model = Platform
    columns = ['id', 'name', 'platform_business_model_type',  'platform_business_model_type', 'description', 'producers', 'consumers']
    order_columns = ['name', 'platform_business_model_type']

    max_display_length = 50

    # def get_initial_queryset(self):
    #     return self.model.objects.all().prefetch_related()
    #
    # def filter_queryset(self, qs):
    #     print(qs)
    #     return qs

    def prepare_results(self, qs):
        # prepare list with output column data
        # queryset is already paginated here
        json_data = []
        for item in qs:
            p_cats = []
            for c in item.platformcategory_set.all():
                p_cats.append(c.category.name)
            t = ""
            if item.platform_business_model_type is not None:
                t = item.platform_business_model_type.name
            json_data.append([
                escape("{0}".format(str(item.id))),
                escape("{0}".format(item.name)),
                escape("{0}".format(t)),
                escape("{0}".format(', '.join(p_cats))),
                escape("{0}".format(item.description)),
                escape("{0}".format(item.producers)),
                escape("{0}".format(item.consumers)),
            ])
        return json_data


class PlatformDetailView(View):
    template_name = 'frontend/platform/platform_details.html'
    page = 'platform'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        platform = Platform.objects.get(pk=pk)
        # industry_categories = PlatformCategory.objects.filter(platform=platform)
        # existing = []
        # for ic in industry_categories:
        #     existing.append(str(ic.category_id))
        # form = PlatformForm(initial={'industry_categories': existing}, instance=platform)
        context = {
            'page': self.page,
            'platform': platform,
            'founded_date': get_formatted_date(platform.founded_date_year, platform.founded_date_month,
                                               platform.founded_date_day),
            'closed_date': get_formatted_date(platform.closed_date_year, platform.closed_date_month,
                                              platform.closed_date_day)
        }
        return render(request, self.template_name, context)