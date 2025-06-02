import axios, {AxiosRequestConfig} from "axios";
import camelcaseKeys from 'camelcase-keys';
import snakecaseKeys from "snakecase-keys";
import {ApiResponse, DataValue, Field} from "../types/api";
import {
    Company,
    ContractorCompany,
    ContractorPerson,
    DocumentData,
    DocumentTemplate,
    ExecutorPerson,
    User
} from "../types/core";

const BASE_API_URL = "http://localhost:8000";
export const ENDPOINTS = {
    COMPANY_REGISTRATION: "/register/company/",

    USER_REGISTRATION: "/register/user/",
    DELETE_USER: (username: string) => `user/delete/${username}/`,
    //USER_REGISTRATION_FIELDS: "/user/values/fields/",

    CONTRACTOR_COMPANY: "/company/contractors/",
    CONTRACTOR_COMPANY_FIELDS: "/company/contractors/fields/",
    DELETE_CONTRACTOR_COMPANY: (companyId: number) => `${ENDPOINTS.CONTRACTOR_COMPANY}${companyId}/`,
    CONTRACTOR_PERSONS: "/persons/contractor/",
    CONTRACTOR_PERSONS_FIELDS: "/persons/contractor/fields/",
    DELETE_CONTRACTOR_PERSONS: (personId: number) => `${ENDPOINTS.CONTRACTOR_PERSONS}${personId}/`,

    COMPANY: "/company/",
    DELETE_COMPANY: "/company/delete/",
    COMPANY_USERS: "/company/users/",
    EXECUTOR_PERSONS: "/persons/executor/",
    EXECUTOR_PERSONS_FIELDS: "/persons/executor/fields/",
    DELETE_EXECUTOR_PERSONS: (personId: number) => `${ENDPOINTS.EXECUTOR_PERSONS}${personId}/`,

    TEMPLATES: "/templates/",
    COMPANY_TEMPLATES: (templateId: number | string = "") => `/templates/company/${templateId}/`,
    TEMPLATE_INFO: (templateId: number) => `templates/${templateId}/info/`,
    
    DOCUMENTS: (templateId: number | string) => `/document/save/${templateId}/`,
    DOCUMENT_TYPES: "/document/types/",
    DOCUMENT_LIST: "/document/list/",

    CHECK_AUTH: "/check_auth/",
    LOGIN: "/login/",
    LOGOUT: "/logout/",
    CSRF: "/csrf/",

    TEMPLATE_FIELDS: (templateId: number) => `/templates/${templateId}/fields/`,
    TEMPLATE_FIELD_FIELDS: (templateId: number) => `/templates/${templateId}/fields/fields/`,
    TEMPLATE_TABLE_FIELD_FIELDS: (templateId: number | string) => `/templates/tables/create/${templateId}/`,
    TEMPLATE_FIELD_VALUES: (templateId: number) => `/templates/tables/${templateId}/`,

    DOWNLOAD_DOCUMENT: (templateId: number) => `/document/download/${templateId}/`,
}

const API_METHODS = {
    GET: "GET",
    POST: "POST",
    PUT: "PUT",
    DELETE: "DELETE",
}

const api = axios.create({
    withCredentials: true,
    baseURL: BASE_API_URL,
    xsrfHeaderName: "X-CSRFToken",
    xsrfCookieName: "csrftoken",
    headers: { "Content-Type": "application/json" },
    timeout: 10000,
    validateStatus: (status) => true // Не считать ошибкой статусы
})

api.interceptors.request.use((config) =>
{
    const data = config.data;
    if (data && config.headers["Content-Type"] === "application/json")
    {
        config.data = toSnake(data);
    }
    return config;
});

api.interceptors.request.use(async (config) =>
{
    if (config.url && config.url !== ENDPOINTS.CSRF)
    {
        config.headers["X-CSRFToken"] = await getCsrfToken();
    }
    return config;
});

api.interceptors.response.use(
    (response) => {
        // Пропускаем преобразование для blob-ответов
        if (response.config.responseType === 'blob') {
            return response;
        }

        const data = response.data;
        if (data) {
            response.data = toCamel(data);
        }
        return response;
    },
    (error) => {
        console.error(error);
        return Promise.reject(error);
    }
);

function toCamel(data: any): any { return camelcaseKeys(data, { deep: true }); }

function toSnake(data: any): any { return snakecaseKeys(data, { deep: true }); }

export async function getCompanyRegistrationFields(): Promise<Field[]>
{
    return await getFields(ENDPOINTS.COMPANY_REGISTRATION);
}

export async function getUserRegistrationFields(): Promise<Field[]>
{
    return await getFields(ENDPOINTS.USER_REGISTRATION);
}

export async function getContractorCompanyFields(): Promise<Field[]>
{
    return await getFields(ENDPOINTS.CONTRACTOR_COMPANY_FIELDS);
}

export async function getContractorPersonFields(): Promise<Field[]>
{
    return await getFields(ENDPOINTS.CONTRACTOR_PERSONS_FIELDS);
}

export async function getExecutorPersonFields(): Promise<Field[]>
{
    return await getFields(ENDPOINTS.EXECUTOR_PERSONS_FIELDS);
}

export async function getLoginFields(): Promise<Field[]>
{
    return await getFields(ENDPOINTS.LOGIN);
}

export async function getDocumentTemplateCreationFields(): Promise<Field[]>
{
    return await getFields(ENDPOINTS.TEMPLATES);
}

export async function getDocumentFields(templateId: number): Promise<Field[]>
{
    return await getFields(ENDPOINTS.DOCUMENTS(templateId));
}

export async function getTemplateFieldsFields(templateId: number): Promise<Field[]>
{
    return await getFields(ENDPOINTS.TEMPLATE_FIELD_FIELDS(templateId));
}

export async function getTemplateTableFieldSettingFields(templateId: number): Promise<Field[]>
{
    return await getFields(ENDPOINTS.TEMPLATE_TABLE_FIELD_FIELDS(templateId))
}

export async function getTemplateTableFieldValues(templateId: number): Promise<Field[]>
{
    return await getFields(ENDPOINTS.TEMPLATE_FIELD_VALUES(templateId));
}

export async function getTemplateInfo(templateId: number): Promise<DocumentTemplate>
{
    return await apiGet<DocumentTemplate>(ENDPOINTS.TEMPLATE_INFO(templateId));
}

async function getFields(url: string): Promise<Field[]>
{
    return await apiGet<Field[]>(url);
}

export async function getCompanyDocumentTemplates(companyId: number): Promise<DocumentTemplate[]>
{
    return await apiGet<DocumentTemplate[]>(ENDPOINTS.COMPANY_TEMPLATES(companyId));
}

export async function getCompany(): Promise<Company>
{
    return await apiGet<Company>(ENDPOINTS.COMPANY);
}

export async function getCompanyUsers(): Promise<User[]>
{
    return await apiGet<User[]>(ENDPOINTS.COMPANY_USERS);
}

export async function getExecutorPersons(): Promise<ExecutorPerson[]>
{
    return await apiGet<ExecutorPerson[]>(ENDPOINTS.EXECUTOR_PERSONS);
}

export async function getContractorCompanies(): Promise<ContractorCompany[]>
{
    return await apiGet<ContractorCompany[]>(ENDPOINTS.CONTRACTOR_COMPANY);
}

export async function getContractorPersons(): Promise<ContractorPerson[]>
{
    return await apiGet<ContractorPerson[]>(ENDPOINTS.CONTRACTOR_PERSONS);
}

export async function getComboboxItems(URL: string): Promise<any[]>
{
    return toSnake(await apiGet<any>(URL));
}

export async function getTemplateTableFields(templateId: number): Promise<Field[]>
{
    return apiGet(ENDPOINTS.TEMPLATE_FIELD_VALUES(templateId));
}

export async function createTemplateField(templateId: number, fieldCreationData: DataValue[]): Promise<any>
{
    return await apiPost<any>({url: ENDPOINTS.TEMPLATE_FIELDS(templateId), body: fieldCreationData});
}

export async function createTemplateTableField(templateId: number, fieldCreationData: DataValue[]): Promise<any>
{
    return await apiPut<any>({url: ENDPOINTS.TEMPLATE_TABLE_FIELD_FIELDS(templateId), body: fieldCreationData});
}

export async function downloadDocument(documentId: number): Promise<void> {
    const url = ENDPOINTS.DOWNLOAD_DOCUMENT(documentId);
    const response = await api.get(url, {
        responseType: 'blob' // Указываем тип ответа - бинарные данные
    });

    // Проверяем статус ответа
    if (!isSuccessfulResponse(response.status)) {
        const errorText = await readBlobAsText(response.data);
        throw new Error(`Ошибка загрузки: ${getFirstOrDefaultErrorMessageFromText(errorText)}`);
    }

    // Извлекаем имя файла из заголовков
    const contentDisposition = response.headers['content-disposition'];
    const fileName = extractFileName(contentDisposition) || `document_${documentId}.docx`;

    // Создаем временную ссылку для скачивания
    const blobUrl = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = blobUrl;
    link.setAttribute('download', fileName);
    document.body.appendChild(link);
    link.click();

    // Убираем элементы после скачивания
    link.parentNode?.removeChild(link);
    window.URL.revokeObjectURL(blobUrl);
}

// Вспомогательные функции
const readBlobAsText = (blob: Blob): Promise<string> => {
    return new Promise((resolve) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result as string);
        reader.readAsText(blob);
    });
};

const getFirstOrDefaultErrorMessageFromText = (text: string): string => {
    try {
        const errorData = JSON.parse(text);
        return errorData.errors?.[0] || text;
    } catch {
        return text;
    }
};

const extractFileName = (contentDisposition: string): string | null => {
    const filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
    const matches = filenameRegex.exec(contentDisposition);
    return matches?.[1]?.replace(/['"]/g, '') || null;
};

export async function createCompany(companyRegistrationData: DataValue[]): Promise<User>
{
    return await apiPost<User>({url: ENDPOINTS.COMPANY_REGISTRATION, body: companyRegistrationData});
}

export async function createUser(userRegistrationData: DataValue[]): Promise<User>
{
    return await apiPost<User>({url: ENDPOINTS.USER_REGISTRATION, body: userRegistrationData});
}

export async function createContractorCompany(userRegistrationData: DataValue[]): Promise<ContractorCompany>
{
    return await apiPost<ContractorCompany>({url: ENDPOINTS.CONTRACTOR_COMPANY_FIELDS, body: userRegistrationData});
}

export async function createContractorPerson(userRegistrationData: DataValue[]): Promise<any>
{
    return await apiPost<ContractorPerson>({url: ENDPOINTS.CONTRACTOR_PERSONS, body: userRegistrationData});
}

export async function createExecutorPerson(userRegistrationData: DataValue[]): Promise<any>
{
    return await apiPost<ExecutorPerson>({url: ENDPOINTS.EXECUTOR_PERSONS, body: userRegistrationData});
}

export async function createDocumentTemplate(templateCreationData: DataValue[]): Promise<DocumentTemplate>
{
    return apiPost({
        url: ENDPOINTS.TEMPLATES,
        body: templateCreationData,
        config: {headers: {"Content-Type": "multipart/form-data"}}});
}

export async function createDocument(templateId: number, documentCreationData: DataValue[]): Promise<DocumentData>
{
    return apiPost<DocumentData>({url: ENDPOINTS.DOCUMENTS(templateId), body: documentCreationData});
}

export async function getDocuments(): Promise<DocumentData[]>
{
    return apiGet<DocumentData[]>(ENDPOINTS.DOCUMENT_LIST);
}

export async function login(userLoginData: DataValue[]): Promise<User>
{
    return await apiPost<User>({url: ENDPOINTS.LOGIN, body: userLoginData})
}

export async function logout()
{
    return await apiPost<void>({url: ENDPOINTS.LOGOUT});
}

export async function getUser(): Promise<User>
{
    return await apiGet<User>(ENDPOINTS.CHECK_AUTH);
}

export async function deleteCompany(): Promise<void>
{
    return await apiDelete(ENDPOINTS.DELETE_COMPANY);
}

export async function deleteCompanyUser(username: string): Promise<void>
{
    return await apiDelete(ENDPOINTS.DELETE_USER(username));
}

export async function deleteContractorPerson(personId: number): Promise<void>
{
    return apiDelete(ENDPOINTS.DELETE_CONTRACTOR_PERSONS(personId));
}

export async function deleteExecutorPerson(personId: number): Promise<void>
{
    return apiDelete(ENDPOINTS.DELETE_EXECUTOR_PERSONS(personId));
}

export async function deleteContractorCompany(companyId: number): Promise<void>
{
    return apiDelete(ENDPOINTS.DELETE_CONTRACTOR_COMPANY(companyId));
}

async function getCsrfToken(): Promise<string>
{
    return await apiGet<string>(ENDPOINTS.CSRF);
}

async function apiGet<TValue>(url: string, config?: AxiosRequestConfig<any>): Promise<TValue>
{
    return await apiRequest<TValue>({ url: url, method: API_METHODS.GET, config: config });
}

async function apiPost<TValue>(options: { url: string, body?: any, config?: AxiosRequestConfig<any>}): Promise<TValue>
{
    return await apiRequest<TValue>({
        url: options.url,
        method: API_METHODS.POST,
        body: options.body,
        config: options.config});
}

async function apiPut<TValue>(options: { url: string, body?: any, config?: AxiosRequestConfig<any>}): Promise<TValue>
{
    return await apiRequest<TValue>({
        url: options.url,
        method: API_METHODS.PUT,
        body: options.body,
        config: options.config});
}

async function apiDelete<TValue = void>(url: string, config?: AxiosRequestConfig<any>): Promise<TValue>
{
    return await apiRequest<TValue>({ url: url, method: API_METHODS.DELETE, config: config });
}

async function apiRequest<TValue>(config: { url: string, method: string, body?: any, config?: AxiosRequestConfig<any> }): Promise<TValue>
{
    const response = await api.request<ApiResponse<TValue>>({...config.config, url: config.url, method: config.method, data: config.body});
    const data = response.data;

    if (config.url !== ENDPOINTS.CSRF) {
        console.log(config.method, config.url, config.body, data);
    }

    if (!isSuccessfulResponse(response.status))
    {
        throw new Error(getFirstOrDefaultErrorMessage(data));
    }

    return data.details as TValue;
}

function isSuccessfulResponse(status: number): boolean
{
    return status >= 200 && status < 300;
}

function getFirstOrDefaultErrorMessage(response: ApiResponse<any>): string
{
    const errors = response.errors;
    if (errors)
    {
        const keys = Object.keys(errors);
        if (keys.length > 0)
        {
            const firstKey = keys[0];
            return `${firstKey}: ${errors[firstKey]}`;
        }
    }
    return "Произошла ошибка при запросе, попробуйте ещё раз";
}