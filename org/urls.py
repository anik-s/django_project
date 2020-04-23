from django.urls import path

from .views.frontend.acquisition import AcquisitionListJson, AcquisitionListView
from .views.frontend.event import EventListJson, EventListView
from .views.frontend.organization import OrganizationListJson, OrganizationListView
from .views.frontend.person import PersonListJson, PersonListView
from .views.frontend.platform import PlatformListJson, PlatformListView, PlatformDetailView

urlpatterns = [

    # platform
    path('platforms/datatable-data', PlatformListJson.as_view(), name='platform_list_json'),
    path('platforms/<pk>', PlatformDetailView.as_view(), name='platform_detail'),
    path('platforms', PlatformListView.as_view(), name='platform_list'),

    # organization
    path('organizations/datatable-data', OrganizationListJson.as_view(), name='organization_list_json'),

    path('organizations', OrganizationListView.as_view(), name='organization_list'),

    # person
    path('persons/datatable-data', PersonListJson.as_view(), name='person_list_json'),

    path('persons', PersonListView.as_view(), name='person_list'),

    # person
    path('acquisitions/datatable-data', AcquisitionListJson.as_view(), name='acquisition_list_json'),

    path('acquisitions', AcquisitionListView.as_view(), name='acquisition_list'),

    # event
    path('events/datatable-data', EventListJson.as_view(), name='event_list_json'),

    path('events', EventListView.as_view(), name='event_list'),

]