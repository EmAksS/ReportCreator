from django.urls import path
from .views import (
    users,
    company,
    documents,
)

urlpatterns = [
    path('csrf/', users.CsrfView.as_view(), name='csrf_token'),
    path('check_auth/', users.AuthCheckView.as_view(), name='check_auth'),
    path('login/', users.UserAuthView.as_view(), name='login'),
    path('logout/', users.UserLogoutView.as_view(), name='logout'),

    path('register/company/', company.register_company, name='register_company'),
    path('register/user/', users.UserRegisterView.as_view(), name='register_user'),
    
    path('company/', company.get_company_info, name='get_company_info'),
    path('company/fields/', company.get_company_fields, name='get_company_fields'),
    path('company/contractors/', company.get_contractors, name='get_contractors'),
    path('company/contractors/fields/', company.get_contractor_fields, name='get_contractor_fields'),
    
    path('persons/executor/list/', company.get_executor_persons, name='executor_list'),
    path('persons/contractor/list/', company.get_contractor_persons, name='contractor_list'),
    path('persons/executor/fields/', company.get_executor_person_fields, name='get_executor_person_fields'),
    path('persons/contractor/fields/', company.get_contractor_person_fields, name='get_contractor_person_fields'),

    path('user/values/', users.UserFieldValueView.as_view(), name='user_fields_values'),
    path('user/values/fields/',users.UserFieldListView.as_view(), name='user_fields'),
    path('user/values/<str:pk>/', users.UserFieldValueDetailView.as_view(), name='field_value_detail'),

    path('templates/company/<int:company_id>/', documents.TemplateCompanyListView.as_view(), name='template_company_list'),
    path('templates/company/current/', documents.TemplateCurrentCompanyListView.as_view(), name='template_current_company_list'),
    path('templates/', documents.TemplateListCreateView.as_view(), name='template_list_create'),
    path('templates/<int:tid>/fields/', documents.TemplateDocumentFieldsListCreateView.as_view(), name='template_fields'),

    # Вставить про документы

    path('document/types/', documents.DocumentTypesView.as_view(), name='document_types'),
]
