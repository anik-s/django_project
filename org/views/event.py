from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.forms import formset_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DeleteView
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from org.forms.event import EventForm, AppearanceFormSet, AppearanceForm
from org.models import Event, EventOrganization, EventPerson, City, EventSubCategory
from org.views.helper import get_formatted_date

page = 'event'


class EventView(LoginRequiredMixin, View):
    template_name = 'dashboard/event/event_add.html'

    def get(self, request, *args, **kwargs):
        form = EventForm()
        children = AppearanceFormSet(prefix="cool")
        context = {
            'operation': 'Create',
            'page': page,
            'form': form,
            'children': children
        }
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = EventForm(self.request.POST, request.FILES)
        if form.data.get('country'):
            form.fields['city'].queryset = City.objects.filter(country_id=form.data.get('country')).order_by('name')
        if form.data.get('category'):
            form.fields['sub_category'].queryset = EventSubCategory.objects.filter(
                event_category_id=form.data.get('category')).order_by('name')
        children = AppearanceFormSet(self.request.POST, prefix='cool')
        form_valid = form.is_valid() and children.is_valid()
        if form_valid:
            event = form.save()
            for c in children:
                c.save(event)
            return redirect('/admin/events')
        else:
            context = {
                'operation': 'Create',
                'page': page,
                'children': children,
                'form': form
            }
            return render(request, self.template_name, context)


class EventUpdateView(LoginRequiredMixin, View):
    template_name = 'dashboard/event/event_add.html'

    success_url = '/admin/events'

    def get(self, request, *args, **kwargs):
        event = Event.objects.get(pk=self.kwargs['pk'])
        form = EventForm()
        form.initial.update({
            'profile_image': event.profile_image,
            'name': event.name,
            'event_type': event.event_type,
            'description': event.description,
            'start_date_year': event.start_date_year,
            'start_date_month': event.start_date_month,
            'start_date_day': event.start_date_day,
            'end_date_year': event.end_date_year,
            'end_date_month': event.end_date_month,
            'end_date_day': event.end_date_day,
            'event_url': event.event_url,
            'registration_url': event.registration_url,
            'full_description': event.full_description,
            'venue_address': event.venue_address,
            'country': event.venue_country,
            'city': event.venue_city,
            'category': event.event_category,
            'sub_category': event.event_sub_category
        })
        form.fields['city'].queryset = City.objects.filter(country_id=event.venue_country_id).order_by('name')
        form.fields['sub_category'].queryset = EventSubCategory.objects.filter(event_category_id=event.event_category_id).order_by('name')

        child = formset_factory(AppearanceForm, extra=0)
        event_person_data = []
        event_persons = EventPerson.objects.filter(event=event)
        for ep in event_persons:
            event_person_data.append({
                'p_type': 'person',
                'appearance_type': ep.appearance_type,
                'person': ep.person
            })
        event_organizations = EventOrganization.objects.filter(event=event)
        for eo in event_organizations:
            event_person_data.append({
                'p_type': 'organization',
                'appearance_type': eo.appearance_type,
                'organization': eo.organization
            })
        children = child(initial=event_person_data, prefix="cool")


        context = {
            'operation': 'Update',
            'page': page,
            'form': form,
            'children': children
        }
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        event = Event.objects.get(pk=self.kwargs['pk'])
        form = EventForm(self.request.POST, request.FILES)
        if form.data.get('country'):
            form.fields['city'].queryset = City.objects.filter(country_id=form.data.get('country')).order_by('name')
        if form.data.get('category'):
            form.fields['sub_category'].queryset = EventSubCategory.objects.filter(
                event_category_id=form.data.get('category')).order_by('name')
        children = AppearanceFormSet(self.request.POST, prefix='cool')
        form_valid = form.is_valid() and children.is_valid()
        if form_valid:
            event = form.update(event)
            # delete existing record from EventPerson and EventOrganization
            EventPerson.objects.filter(event=event).delete()
            EventOrganization.objects.filter(event=event).delete()
            # entry new record to EventPerson and EventOrganization
            for c in children:
                c.save(event)
            return redirect('/admin/events')
        else:
            context = {
                'operation': 'Update',
                'page': page,
                'children': children,
                'form': form
            }
            return render(request, self.template_name, context)


@login_required
def get_cities(request):
    country_id = request.GET.get('country')
    cities = []
    if country_id:
        cities = City.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'dashboard/common/city_options.html', {'cities': cities})


@login_required
def get_subcategories(request):
    category_id = request.GET.get('categoryId')
    sub_categories = []
    if category_id:
        sub_categories = EventSubCategory.objects.filter(event_category_id=category_id).order_by('name')
    return render(request, 'dashboard/common/event_sub_category_options.html', {'sub_categories': sub_categories})


class EventListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, "dashboard/event/event_list.html", {'page': page})


class EventListJson(LoginRequiredMixin, BaseDatatableView):
    model = Event
    # define the columns that will be returned
    columns = ['id', 'name', 'start_date_year', 'venue_city', 'venue_country', 'id']
    order_columns = ['id', 'name', 'venue_city', 'venue_country']

    # def get_initial_queryset(self):
    #     return Event.objects.all()

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 50

    # def render_column(self, row, column):
    #     # We want to render user as a custom column
    #     # if column == 'user':
    #     #     # escape HTML for security reasons
    #     #     return escape('{0} {1}'.format(row.first_name, row.first_name))
    #     # else:
    #     return super(PersonListJson, self).render_column(row, column)

    # def filter_queryset(self, qs):
    #     print(qs)

    def prepare_results(self, qs):
        # prepare list with output column data
        # queryset is already paginated here
        json_data = []
        for item in qs:
            # print(item.country)
            city = ""
            country = ""
            if item.venue_city is not None:
                city = item.venue_city.name
            if item.venue_country is not None:
                country = item.venue_country.name

            json_data.append([
                escape("{0}".format(str(item.id))),
                escape("{0}".format(item.name)),
                escape(get_formatted_date(item.start_date_year, item.start_date_month, item.start_date_day)),
                escape("{0}".format(city)),
                escape("{0}".format(country)),
                escape("{0}".format(str(item.id))),
            ])
        return json_data


class EventDeleteView(DeleteView):
    model = Event
    # template_name = "dashboard/person/person_delete.html"
    # success_url = reverse_lazy('person_list')

    def delete(self, request, *args, **kwargs):
        try:
            self.get_object().delete()
            payload = {'status': True}
            return JsonResponse(payload, status=200)
        except Exception as e:
            return JsonResponse({'status': False}, status=500)