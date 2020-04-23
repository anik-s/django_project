from django.contrib import admin
from .models import EventType, Country, City, EventCategory, EventSubCategory, AppearanceType, Person, Organization, \
    CompanyType, OrganizationType, InvestorType, InvestmentStage, OrganizationCategory, PlatformBusinessModelType, \
    StockExchange, Currency, Disposition, AcquisitionTerm, AcquisitionStatus, AcquisitionType, Acquisition, \
    Platform, FundingRound, FundingType, FundingRoundInvestor, FundingRoundInvestorOrganization, JobPosition, \
    InvestorStage, Gender, PersonType, OrganizationSubCategory, OrganizationRelation

# Register your models here.

admin.site.register(Country)
admin.site.register(City)
admin.site.register(EventCategory)
admin.site.register(EventSubCategory)
admin.site.register(AppearanceType)
admin.site.register(Person)
admin.site.register(EventType)
admin.site.register(Organization)
admin.site.register(CompanyType)
admin.site.register(OrganizationType)
admin.site.register(InvestorType)
admin.site.register(InvestmentStage)
admin.site.register(OrganizationCategory)
admin.site.register(PlatformBusinessModelType)
admin.site.register(StockExchange)
admin.site.register(Currency)
admin.site.register(Disposition)
admin.site.register(AcquisitionStatus)
admin.site.register(AcquisitionType)
admin.site.register(AcquisitionTerm)
admin.site.register(Platform)
admin.site.register(FundingRoundInvestorOrganization)
admin.site.register(FundingRoundInvestor)
admin.site.register(FundingType)
admin.site.register(FundingRound)
admin.site.register(Acquisition)
admin.site.register(InvestorStage)
admin.site.register(JobPosition)
admin.site.register(Gender)
admin.site.register(PersonType)
admin.site.register(OrganizationSubCategory)
admin.site.register(OrganizationRelation)
