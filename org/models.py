import uuid

from django.db import models
from django.contrib.auth.models import User


class EventType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "event_types"


class EventCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "event_categories"


class EventSubCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    event_category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "event_sub_categories"


class Country(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "countries"


class City(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "cities"


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile_image = models.ImageField(max_length=2056, upload_to='event', default=None)
    name = models.CharField(max_length=1000)
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    description = models.TextField()
    start_date_year = models.CharField(max_length=4, blank=True)
    start_date_month = models.CharField(max_length=14, blank=True)
    start_date_day = models.CharField(max_length=4, blank=True)
    end_date_year = models.CharField(max_length=4, blank=True)
    end_date_month = models.CharField(max_length=14, blank=True)
    end_date_day = models.CharField(max_length=4, blank=True)
    event_url = models.URLField(null=True)
    registration_url = models.URLField(null=True)
    full_description = models.TextField(null=True)
    venue_address = models.TextField(null=True)
    venue_country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    venue_city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
    event_sub_category = models.ForeignKey(EventSubCategory, on_delete=models.CASCADE, null=True)
    event_category = models.ForeignKey(EventCategory, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "events"


class InvestmentStage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "investment_stages"


class Gender(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "genders"


class PersonType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "person_types"


class InvestorStage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "investor_stages"


class Person(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile_image = models.ImageField(max_length=2056, upload_to='person', default=None)
    type = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    gender = models.ForeignKey(Gender, null=True, default=None, on_delete=models.CASCADE)
    aka = models.CharField(max_length=100, null=True, default=None, )
    investor_stage = models.ForeignKey(InvestorStage, null=True, default=None, on_delete=models.CASCADE)
    website = models.URLField(null=True, blank=True, default='')
    facebook = models.URLField(null=True, blank=True, )
    linkedin = models.URLField(null=True, blank=True, )
    twitter = models.URLField(null=True, blank=True, )
    biography = models.TextField(null=True, blank=True)
    country = models.ForeignKey(Country, null=True, on_delete=models.CASCADE)
    city = models.ForeignKey(City, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name

    class Meta:
        db_table = "persons"


class JobPosition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "job_positions"


class PersonJob(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    position = models.ForeignKey(JobPosition, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    start_date_year = models.CharField(max_length=4, blank=True)
    start_date_month = models.CharField(max_length=14, blank=True)
    start_date_day = models.CharField(max_length=2, blank=True)
    has_end_date = models.BooleanField(null=True)
    end_date_year = models.CharField(max_length=4, blank=True)
    end_date_month = models.CharField(max_length=14, blank=True)
    end_date_day = models.CharField(max_length=2, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "person_jobs"


class OrganizationType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "organization_types"


class CompanyType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "company_types"


class InvestorType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "investor_types"


class OrganizationCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "organization_categories"


class OrganizationSubCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(OrganizationCategory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "organization_sub_categories"


class PlatformBusinessModelType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "platform_business_model_types"


class StockExchange(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "stock_exchanges"


class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile_image = models.ImageField(max_length=2056, upload_to='organization', default=None, null=True)
    organization_type = models.CharField(max_length=100)
    name = models.CharField(max_length=1000)
    description = models.TextField()
    aka = models.CharField(max_length=1000, null=True)
    legal_name = models.CharField(max_length=1000, null=True)

    founded_date_year = models.CharField(max_length=4, blank=True)
    founded_date_month = models.CharField(max_length=14, blank=True)
    founded_date_day = models.CharField(max_length=2, blank=True)

    closed_date_year = models.CharField(max_length=4, blank=True)
    closed_date_month = models.CharField(max_length=14, blank=True)
    closed_date_day = models.CharField(max_length=2, blank=True)

    number_of_employees = models.CharField(max_length=100, null=True, blank=True)

    # in case of organization is a type of company
    company_type = models.ForeignKey(CompanyType, on_delete=models.CASCADE, null=True)

    # in case of organization is a type of investment firm
    investor_type = models.ForeignKey(InvestorType, on_delete=models.CASCADE, null=True)
    investment_stage = models.ForeignKey(InvestmentStage, on_delete=models.CASCADE, null=True)

    website = models.URLField(null=True)
    facebook = models.URLField(null=True)
    linkedin = models.URLField(null=True)
    twitter = models.URLField(null=True)
    contact_email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=100, null=True)

    full_description = models.TextField(null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)

    # industry_category = models.ForeignKey(OrganizationCategory, on_delete=models.CASCADE)
    platform_business_mode_type = models.ForeignKey(PlatformBusinessModelType, null=True, on_delete=models.CASCADE)

    stock_symbol = models.CharField(max_length=1000, null=True)
    stock_exchange = models.ForeignKey(StockExchange, on_delete=models.CASCADE, null=True)

    ipo_date_year = models.CharField(max_length=4, blank=True)
    ipo_date_month = models.CharField(max_length=14, blank=True)
    ipo_date_day = models.CharField(max_length=2, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "organizations"


class CompanyFounder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "company_founders"


class OrganizationHasCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    category = models.ForeignKey(OrganizationSubCategory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "organization_has_categories"


class OrganizationRelation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "organization_relations"


class OrgSubOrganization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='organization')
    sub_organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='sub_organization')
    relation = models.ForeignKey(OrganizationRelation, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = "org_sub_organizations"


class AppearanceType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "appearance_types"


class EventOrganization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    appearance_type = models.ForeignKey(AppearanceType, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "event_organizations"


class EventPerson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    appearance_type = models.ForeignKey(AppearanceType, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "event_persons"


class AcquisitionType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "acquisition_types"


class AcquisitionStatus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "acquisition_statuses"


class AcquisitionTerm(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "acquisition_terms"


class Disposition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "dispositions"


class Currency(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "currencies"


class Acquisition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction_name = models.CharField(max_length=500)
    acquiring_organization = models.ForeignKey(Organization, on_delete=models.CASCADE,
                                               related_name='acquiring_organization')
    acquired_organization = models.ForeignKey(Organization, on_delete=models.CASCADE,
                                              related_name='acquired_organization')

    announced_date_year = models.CharField(max_length=4, blank=True)
    announced_date_month = models.CharField(max_length=14, blank=True)
    announced_date_day = models.CharField(max_length=2, blank=True)

    completed_date_year = models.CharField(max_length=4, blank=True)
    completed_date_month = models.CharField(max_length=14, blank=True)
    completed_date_day = models.CharField(max_length=2, blank=True)

    price = models.DecimalField(max_digits=15, decimal_places=2, null=True, default=None)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, default=None)

    acquisition_type = models.ForeignKey(AcquisitionType, null=True, on_delete=models.CASCADE)
    acquisition_status = models.ForeignKey(AcquisitionStatus, null=True, on_delete=models.CASCADE)
    disposition = models.ForeignKey(Disposition, null=True, on_delete=models.CASCADE)
    acquisition_term = models.ForeignKey(AcquisitionTerm, null=True, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "acquisitions"


class FundingType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "funding_types"


class FundingRound(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    investee_organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    funding_type = models.ForeignKey(FundingType, on_delete=models.CASCADE)

    announced_date_year = models.CharField(max_length=4, blank=True)
    announced_date_month = models.CharField(max_length=14, blank=True)
    announced_date_day = models.CharField(max_length=2, blank=True)

    closed_date_year = models.CharField(max_length=4, blank=True)
    closed_date_month = models.CharField(max_length=14, blank=True)
    closed_date_day = models.CharField(max_length=2, blank=True)

    money_raised = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    money_raised_currency = models.ForeignKey(Currency, null=True, on_delete=models.CASCADE,
                                              related_name='money_raised_currency')

    target_funding = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    target_funding_currency = models.ForeignKey(Currency, null=True, on_delete=models.CASCADE,
                                                related_name='target_funding_currency')

    pre_money_valuation = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    pre_money_valuation_currency = models.ForeignKey(Currency, null=True, on_delete=models.CASCADE,
                                                     related_name='pre_money_valuation_currency')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "funding_rounds"


class FundingRoundInvestor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    funding_round = models.ForeignKey(FundingRound, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    lead_investor = models.BooleanField(null=True)
    money_raised = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    money_raised_currency = models.ForeignKey(Currency, null=True, on_delete=models.CASCADE,
                                              related_name='person_money_raised_currency')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "funding_round_investors"


class FundingRoundInvestorOrganization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    funding_round = models.ForeignKey(FundingRound, on_delete=models.CASCADE)
    investor_organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    lead_investor = models.BooleanField(null=True)
    money_raised = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    money_raised_currency = models.ForeignKey(Currency, null=True, on_delete=models.CASCADE,
                                              related_name='organization_money_raised_currency')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "funding_round_investor_organizations"


class Platform(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile_image = models.ImageField(max_length=2056, upload_to='platform', default=None)
    name = models.CharField(max_length=1000)
    description = models.TextField()

    founded_date_year = models.CharField(max_length=4, blank=True)
    founded_date_month = models.CharField(max_length=14, blank=True)
    founded_date_day = models.CharField(max_length=2, blank=True)

    closed_date_year = models.CharField(max_length=4, blank=True)
    closed_date_month = models.CharField(max_length=14, blank=True)
    closed_date_day = models.CharField(max_length=2, blank=True)

    website = models.URLField()
    facebook = models.URLField()
    linkedin = models.URLField()
    twitter = models.URLField()
    contact_email = models.EmailField()
    phone_number = models.CharField(max_length=100)
    full_description = models.TextField()
    owned_by_organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    platform_business_model_type = models.ForeignKey(PlatformBusinessModelType, on_delete=models.CASCADE, null=True)
    producers = models.TextField()
    consumers = models.TextField()
    partners = models.TextField()
    transactions = models.TextField()
    value = models.TextField()
    network_effects = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "platforms"


class PlatformCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    category = models.ForeignKey(OrganizationSubCategory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "platform_categories"


class News(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.TextField()
    url = models.URLField(null=True)
    date_year = models.CharField(max_length=4, blank=True)
    date_month = models.CharField(max_length=14, blank=True)
    date_day = models.CharField(max_length=2, blank=True)
    publisher = models.CharField(max_length=1000, null=True)
    thumbnail_url = models.URLField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "news"


class PersonNews(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "people_news"


class OrganizationNews(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "organization_news"


class FundingNews(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    funding = models.ForeignKey(FundingRound, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "funding_news"


class EventNews(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "event_news"


class PlatformNews(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "platform_news"


class AcquisitionNews(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    acquisition = models.ForeignKey(Acquisition, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "acquisition_news"


class Acquisition2(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    appearance_type = models.ForeignKey(AppearanceType, on_delete=models.CASCADE)

    class Meta:
        db_table = "acquisitions3"


class SiteAdmin(User):
    class Meta:
        proxy = True

