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

    path('register/company/', company.CompanyRegisterView.as_view(), name='register_company'),
    path('register/user/', users.UserRegisterView.as_view(), name='register_user'),
    
    path('company/', company.CompanyInfoView.as_view(), name='get_company_info'),
    path('company/users/', company.CompanyUsersView.as_view(), name='get_company_users'),
    path('company/fields/', company.CompanyRegisterView.as_view(), name='get_company_fields'),
    path('company/contractors/', company.ContractorListView.as_view(), name='get_contractors'),
    path('company/contractors/fields/', company.ContractorCreateView.as_view(), name='get_contractor_fields'),
    
    path('persons/executor/', company.ExecutorPersonListCreateView.as_view(), name='executor_list'),
    path('persons/contractor/', company.ContractorPersonListCreateView.as_view(), name='contractor_list'),
    path('persons/executor/<int:pk>/', company.ExecutorPersonDetailView.as_view(), name='executor_person_detail'),
    path('persons/contractor/<int:pk>/', company.ContractorPersonDetailView.as_view(), name='contractor_person_detail'),
    path('persons/executor/fields/', company.ExecutorPersonFieldsListView.as_view(), name='get_executor_person_fields'),
    path('persons/contractor/fields/', company.ContractorPersonFieldsListView.as_view(), name='get_contractor_person_fields'),

    path('user/values/', users.UserFieldValueView.as_view(), name='user_fields_values'),
    path('user/values/fields/',users.UserFieldListView.as_view(), name='user_fields'),
    path('user/values/<str:pk>/', users.UserFieldValueDetailView.as_view(), name='field_value_detail'),

    path('templates/company/<int:company_id>/', documents.TemplateCompanyListView.as_view(), name='template_company_list'),
    path('templates/company/current/', documents.TemplateCurrentCompanyListView.as_view(), name='template_current_company_list'),
    path('templates/', documents.TemplateListCreateView.as_view(), name='template_list_create'),
    path('templates/<int:pk>/', documents.TemplateDetailDestroyView.as_view(), name='template_detail'),
    path('templates/<int:tid>/info/', documents.TemplateInfoView.as_view(), name='template_info'),
    path('templates/<int:tid>/fields/', documents.TemplateDocumentFieldsListCreateView.as_view(), name='template_fields'),
    path('templates/<int:tid>/fields/fields/', documents.TemplateDocumentFieldsFieldsView.as_view(), name='template_fields_fields_view'),
    path('templates/tables/create/', documents.TableFieldsListCreateView.as_view(), name='template_table_create'),
    path('templates/tables/<int:tk>/', documents.TemplateTableFieldsListView.as_view(), name='template_table_view'),

    # Вставить про документы
    path('document/save/<int:tid>/', documents.DocumentFieldsCreateView.as_view(), name='document_create'),

    path('document/types/', documents.DocumentTypesView.as_view(), name='document_types'),
    path('field/types/', documents.FieldTypesView.as_view(), name='field_types'),
]
