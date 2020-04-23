from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.forms import formset_factory
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import UpdateView, CreateView, DeleteView
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape

from org.forms.news import NewsForm, MentionFormSet, NewsMentionForm
from org.models import News, PersonNews, OrganizationNews, PlatformNews, FundingNews, AcquisitionNews, EventNews
from org.views.helper import get_formatted_date

page = 'news'


class NewsCreateView(LoginRequiredMixin, CreateView):
    template_name = 'dashboard/news/news_add.html'
    form_class = NewsForm
    model = News
    success_url = '/admin/news'

    def get_context_data(self, **kwargs):
        ctx = super(NewsCreateView, self).get_context_data(**kwargs)
        if self.request.method == 'GET':
            ctx['mention_form_set'] = MentionFormSet(prefix="mention")
        elif self.request.method == 'POST':
            ctx['mention_form_set'] = MentionFormSet(self.request.POST, prefix="mention")
        ctx['page'] = page
        ctx['operation'] = 'Create'
        return ctx

    @transaction.atomic
    def form_valid(self, form):
        # data = form.cleaned_data
        mention_form_set = MentionFormSet(self.request.POST, prefix='mention')
        if not mention_form_set.is_valid():
            return super(NewsCreateView, self).form_invalid(form)
        news = form.save()
        for mention_form in mention_form_set:
            mention_form.save(news)
        return super().form_valid(form)


class NewsUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'dashboard/news/news_add.html'
    form_class = NewsForm
    success_url = '/admin/news'
    model = News

    def get_initial(self):
        initial = super(NewsUpdateView, self).get_initial()
        return initial

    def get_context_data(self, **kwargs):
        ctx = super(NewsUpdateView, self).get_context_data(**kwargs)
        if self.request.method == 'GET':
            news = News.objects.get(pk=self.kwargs['pk'])
            mention_form = formset_factory(NewsMentionForm, extra=0)
            mention_data = []
            person_news = PersonNews.objects.filter(news=news)
            for pn in person_news:
                mention_data.append({'mention_type': 'person', 'person': pn.person})
            organization_news = OrganizationNews.objects.filter(news=news)
            for on in organization_news:
                mention_data.append({'mention_type': 'organization', 'organization': on.organization})
            platform_news = PlatformNews.objects.filter(news=news)
            for p_n in platform_news:
                mention_data.append({'mention_type': 'platform', 'platform': p_n.platform})
            funding_news = FundingNews.objects.filter(news=news)
            for fn in funding_news:
                mention_data.append({'mention_type': 'funding_round', 'funding_round': fn.funding})
            acquisition_news = AcquisitionNews.objects.filter(news=news)
            for an in acquisition_news:
                mention_data.append({'mention_type': 'acquisition', 'acquisition': an.acquisition})
            event_news = EventNews.objects.filter(news=news)
            for en in event_news:
                mention_data.append({'mention_type': 'event', 'event': en.event})
            ctx['mention_form_set'] = mention_form(initial=mention_data, prefix="mention")
        elif self.request.method == 'POST':
            ctx['mention_form_set'] = MentionFormSet(self.request.POST, prefix="mention")
        ctx['page'] = page
        ctx['operation'] = 'Update'
        return ctx

    @transaction.atomic
    def form_valid(self, form):
        # data = form.cleaned_data
        mention_form_set = MentionFormSet(self.request.POST, prefix='mention')
        if not mention_form_set.is_valid():
            return super(NewsUpdateView, self).form_invalid(form)
        news = form.save()
        # delete existing records
        PersonNews.objects.filter(news=news).delete()
        OrganizationNews.objects.filter(news=news).delete()
        PlatformNews.objects.filter(news=news).delete()
        AcquisitionNews.objects.filter(news=news).delete()
        FundingNews.objects.filter(news=news).delete()
        EventNews.objects.filter(news=news).delete()
        # entry new records
        for mention_form in mention_form_set:
            mention_form.save(news)
        return super().form_valid(form)


class NewsListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, "dashboard/news/news_list.html", {'page': page})


class NewsListJson(LoginRequiredMixin, BaseDatatableView):
    model = News
    # define the columns that will be returned
    columns = ['id', 'title', 'created_at', 'id']
    order_columns = ['id', 'title', 'created_at']

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 20

    # def render_column(self, row, column):
    #     # We want to render user as a custom column
    #     # if column == 'user':
    #     #     # escape HTML for security reasons
    #     #     return escape('{0} {1}'.format(row.first_name, row.first_name))
    #     # else:
    #     return super(PersonListJson, self).render_column(row, column)

    def prepare_results(self, qs):
        # prepare list with output column data
        # queryset is already paginated here
        json_data = []
        for item in qs:
            json_data.append([
                escape("{0}".format(str(item.id))),
                escape("{0}".format(item.title)),
                escape(get_formatted_date(item.date_year, item.date_month, item.date_day)),
                escape("{0}".format(str(item.id))),
            ])
        return json_data


class NewsDeleteView(LoginRequiredMixin, DeleteView):

    model = News

    def delete(self, request, *args, **kwargs):
        try:
            self.get_object().delete()
            payload = {'status': True}
            return JsonResponse(payload, status=200)
        except Exception as e:
            return JsonResponse({'status': False}, status=500)