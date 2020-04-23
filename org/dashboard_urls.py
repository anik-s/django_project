from django.urls import path, include
from django.contrib.auth import views as auth_views

from .forms.login import LoginForm
from .views.event import EventView, EventUpdateView, EventDeleteView, EventListJson, EventListView
from .views.event import get_cities, get_subcategories
from .views.acquisition import AcquisitionCreateView, AcquisitionUpdateView, AcquisitionDeleteView, AcquisitionListJson, \
    AcquisitionListView
from . import vi
from .views.funding_round import FundingRoundCreateView, FundingRoundUpdateView, FundingRoundDeleteView, \
    FundingRoundListJson, FundingRoundListView
from .views.langing import landing_page
from .views.news import NewsCreateView, NewsUpdateView, NewsDeleteView, NewsListView, NewsListJson
from .views.organization import OrganizationCreateView, OrganizationUpdateView, OrganizationListJson, \
    OrganizationListView, OrganizationDeleteView
from .views.person import PersonCreateView, PersonUpdateView, PersonListJson, PersonListView, PersonDeleteView
from .views.platform import PlatformCreateView, PlatformUpdateView, PlatformDeleteView, PlatformListJson, \
    PlatformListView
from .views.site_admin import SiteAdminCreateView, SiteAdminListView, SiteAdminListJson, SiteAdminDeleteView, \
    SiteAdminUpdateView, PasswordChangeView

urlpatterns = [

    # landing page
    path('', landing_page, name='landing_page'),

    # event
    path('events/<pk>/update', EventUpdateView.as_view(), name='event_update'),
    path('events/<pk>/delete', EventDeleteView.as_view(), name='event_delete'),
    path('events/add', EventView.as_view(), name='event_add'),
    path('events/datatable-data', EventListJson.as_view(), name='event_list_json'),
    path('events', EventListView.as_view(), name='event_list'),

    # acquisition
    path('acquisitions/<pk>/update', AcquisitionUpdateView.as_view(), name='acquisition_update'),
    path('acquisitions/<pk>/delete', AcquisitionDeleteView.as_view(), name='acquisition_round_delete'),
    path('acquisitions/add', AcquisitionCreateView.as_view(), name='acquisition_add'),
    path('acquisitions/datatable-data', AcquisitionListJson.as_view(), name='acquisition_list_json'),
    path('acquisitions', AcquisitionListView.as_view(), name='acquisition_list'),

    # news
    path('news/<pk>/update', NewsUpdateView.as_view(), name='news_update'),
    path('news/<pk>/delete', NewsDeleteView.as_view(), name='news_delete'),
    path('news/add', NewsCreateView.as_view(), name='news_add'),
    path('news/datatable-data', NewsListJson.as_view(), name='news_list_json'),
    path('news', NewsListView.as_view(), name='news_list'),

    # person
    path('persons/<pk>/update', PersonUpdateView.as_view(), name='person_update'),
    path('persons/<pk>/delete', PersonDeleteView.as_view(), name='person_delete'),
    path('persons/add', PersonCreateView.as_view(), name='person_add'),
    path('persons/datatable-data', PersonListJson.as_view(), name='person_list_json'),
    path('persons', PersonListView.as_view(), name='person_list'),

    # platform
    path('platforms/<pk>/update', PlatformUpdateView.as_view(), name='platform_update'),
    path('platforms/<pk>/delete', PlatformDeleteView.as_view(), name='platform_delete'),
    path('platforms/add', PlatformCreateView.as_view(), name='platform_add'),
    path('platforms/datatable-data', PlatformListJson.as_view(), name='platform_list_json'),
    path('platforms', PlatformListView.as_view(), name='platform_list'),

    # organization
    path('organizations/<pk>/update', OrganizationUpdateView.as_view(), name='organizations_update'),
    path('organizations/<pk>/delete', OrganizationDeleteView.as_view(), name='organization_delete'),
    path('organizations/add', OrganizationCreateView.as_view(), name='organization_add'),
    path('organizations/datatable-data', OrganizationListJson.as_view(), name='organization_list_json'),
    path('organizations', OrganizationListView.as_view(), name='organization_list'),

    # funding round
    path('funding_rounds/<pk>/update', FundingRoundUpdateView.as_view(), name='funding_round_update'),
    path('funding_rounds/<pk>/delete', FundingRoundDeleteView.as_view(), name='funding_round_delete'),
    path('funding_rounds/add', FundingRoundCreateView.as_view(), name='funding_round_add'),
    path('funding_rounds/datatable-data', FundingRoundListJson.as_view(), name='funding_round_list_json'),
    path('funding_rounds', FundingRoundListView.as_view(), name='funding_round_list'),

    # site admins
    path('site-admins/<pk>/delete', SiteAdminDeleteView.as_view(), name='site_admin_delete'),
    path('site-admins/<pk>/update', SiteAdminUpdateView.as_view(), name='site_admin_update'),
    path('site-admins/add', SiteAdminCreateView.as_view(), name='site_admin_add'),
    path('site-admins/datatable-data', SiteAdminListJson.as_view(), name='site_admin_list_json'),
    path('site-admins', SiteAdminListView.as_view(), name='site_admin_list'),
    path('settings', PasswordChangeView.as_view(), name='settings'),

    # auth
    path('login/', auth_views.LoginView.as_view(template_name='dashboard/public/public_base1.html',
                                                authentication_form=LoginForm)),
    path('logout/', auth_views.LogoutView.as_view(next_page='/admin/login/')),

    # select2
    path('select2', include('django_select2.urls')),

    # others
    path('ajax/load-cities/', get_cities, name='ajax_get_cities'),
    path('ajax/event-subcategories/', get_subcategories, name='ajax_get_subcategories'),
]
