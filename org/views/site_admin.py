from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DeleteView
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape

from org.forms.password_change import PasswordChangeForm
from org.forms.site_admin import SiteAdminForm
from org.models import SiteAdmin


page = 'site_admin'


class SiteAdminCreateView(LoginRequiredMixin, View):
    template_name = 'dashboard/site_admin/site_admin_add.html'

    def get(self, request, *args, **kwargs):
        form = SiteAdminForm()
        context = {
            'page': page,
            'operation': "Create",
            'form': form
        }
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = SiteAdminForm(self.request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            site_admin = SiteAdmin.objects.create_user(username=username, email=email, password=password)
            return redirect('/admin/site-admins')
        else:
            context = {
                'page': page,
                'operation': "Create",
                'form': form
            }
            return render(request, self.template_name, context)


class SiteAdminUpdateView(LoginRequiredMixin, View):
    template_name = 'dashboard/site_admin/site_admin_add.html'
    success_url = '/admin/site-admins'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        site_admin = SiteAdmin.objects.get(pk=pk)
        form = SiteAdminForm(initial={
            'username': site_admin.username,
            'email': site_admin.email,
            'password': ''
        })
        context = {
            'page': page,
            'operation': "Update",
            'form': form
        }
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        site_admin = SiteAdmin.objects.get(pk=pk)
        form = SiteAdminForm(self.request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            site_admin.username = username
            site_admin.email = email
            site_admin.set_password(password)
            site_admin.save()
            return redirect('/admin/site-admins')
        else:
            context = {
                'page': page,
                'operation': "Update",
                'form': form
            }
            return render(request, self.template_name, context)


class SiteAdminListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, "dashboard/site_admin/site_admin_list.html", {'page': page})


class SiteAdminListJson(LoginRequiredMixin, BaseDatatableView):
    model = SiteAdmin
    # define the columns that will be returned
    columns = ['id', 'username', 'email', 'date_joined', 'id']
    order_columns = ['id', 'username', 'email', 'date_joined']

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
                escape("{0}".format(item.username)),
                escape("{0}".format(item.email)),
                item.date_joined.strftime("%d-%m-%y"),
                escape("{0}".format(str(item.id))),
            ])
        return json_data


class SiteAdminDeleteView(LoginRequiredMixin, DeleteView):

    model = SiteAdmin

    def delete(self, request, *args, **kwargs):
        try:
            self.get_object().delete()
            payload = {'status': True}
            return JsonResponse(payload, status=200)
        except Exception as e:
            return JsonResponse({'status': False}, status=500)


class PasswordChangeView(LoginRequiredMixin, View):
    template_name = 'dashboard/site_admin/password_change.html'

    def get(self, request, *args, **kwargs):
        form = PasswordChangeForm()
        context = {
            'page': 'settings',
            'operation': "Update",
            'form': form
        }
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(self.request.POST)
        site_admin = request.user
        if form.is_valid():
            password = form.cleaned_data.get('password')
            site_admin.set_password(password)
            site_admin.save()
            return redirect('/admin')
        else:
            context = {
                'page': 'settings',
                'operation': "Update",
                'form': form
            }
            return render(request, self.template_name, context)