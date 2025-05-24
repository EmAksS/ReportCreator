import axios from "axios";
import camelcaseKeys from 'camelcase-keys';
import snakecaseKeys from "snakecase-keys";
import {ApiResponse, DataValue, Field} from "../types/api";
import {Company, ContractorCompany, ContractorPerson, ExecutorPerson, User} from "../types/core";

const BASE_API_URL = "http://localhost:8000";
export const ENDPOINTS = {
    COMPANY_REGISTRATION: "/register/company/",

    USER_REGISTRATION: "/register/user/",
    USER_REGISTRATION_FIELDS: "/user/values/fields/",

    CONTRACTOR_COMPANY: "/company/contractors/",
    CONTRACTOR_COMPANY_FIELDS: "/company/contractors/fields/",
    CONTRACTOR_PERSONS: "/persons/contractor/",
    CONTRACTOR_PERSONS_FIELDS: "/persons/contractor/fields/",

    COMPANY: "/company/",
    COMPANY_USERS: "/company/users",
    EXECUTOR_PERSONS: "/persons/executor/",
    EXECUTOR_PERSONS_FIELDS: "/persons/executor/fields/",

    TEMPLATES: "/templates/",

    CHECK_AUTH: "/check_auth/",
    LOGIN: "/login/",
    LOGOUT: "/logout/",
    CSRF: "/csrf/"
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
    (response) =>
    {
        const data = response.data;
        if (data)
        {
            response.data = toCamel(data);
        }
        return response;
    },
    (error) =>
    {
        console.error(error);
        return Promise.reject(error);
    });

function toCamel(data: any): any { return camelcaseKeys(data, { deep: true }); }

function toSnake(data: any): any { return snakecaseKeys(data, { deep: true }); }

export async function getCompanyRegistrationFields(): Promise<Field[]>
{
    return await getFields(ENDPOINTS.COMPANY_REGISTRATION);
}

export async function getUserRegistrationFields(): Promise<Field[]>
{
    return await getFields(ENDPOINTS.USER_REGISTRATION_FIELDS);
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

export async function getDocumentTemplateFields(): Promise<Field[]>
{
    return await getFields(ENDPOINTS.TEMPLATES);
}


export async function getCompany(): Promise<Company>
{
    return (await api.get<Company>(ENDPOINTS.COMPANY)).data;
}

export async function getCompanyUsers(): Promise<User[]>
{
    return (await api.get<User[]>(ENDPOINTS.COMPANY_USERS)).data;
}

export async function getExecutorPersons(): Promise<ExecutorPerson[]>
{
    return (await api.get<ExecutorPerson[]>(ENDPOINTS.EXECUTOR_PERSONS)).data;
}

export async function getContractorCompanies(): Promise<ContractorCompany[]>
{
    return (await api.get<ContractorCompany[]>(ENDPOINTS.CONTRACTOR_COMPANY)).data
}

export async function getContractorPersons(): Promise<ContractorPerson[]>
{
    return (await api.get<ContractorPerson[]>(ENDPOINTS.CONTRACTOR_PERSONS)).data
}

export async function getComboboxItems(URL: string): Promise<any[]>
{
    const response = await api.get(URL);
    return toSnake(response.data);
}

export async function createCompany(companyRegistrationData: DataValue[]): Promise<User>
{
    const response = await api.post<DataValue[], ApiResponse<User>>(ENDPOINTS.COMPANY_REGISTRATION, companyRegistrationData);
    if (!response.details) throw new Error();
    return response.details
}

export async function createUser(userRegistrationData: DataValue[]): Promise<User>
{
    const response = await api.post<ApiResponse<User>>(ENDPOINTS.USER_REGISTRATION, userRegistrationData);
    if (!response.data.details) throw new Error("Не удалось зарегистрировать пользователя");
    return response.data.details
}

export async function createContractorCompany(userRegistrationData: DataValue[]): Promise<ContractorCompany>
{
    const response = await api.post<ApiResponse<ContractorCompany>>(ENDPOINTS.CONTRACTOR_COMPANY_FIELDS, userRegistrationData);
    return response.data.details as ContractorCompany;
}

export async function createContractorPerson(userRegistrationData: DataValue[]): Promise<any>
{
    const response = await api.post<any>(ENDPOINTS.CONTRACTOR_PERSONS, userRegistrationData);
    return response.data.details
}

export async function createExecutorPerson(userRegistrationData: DataValue[]): Promise<any>
{
    const response = await api.post<ApiResponse<any>>(ENDPOINTS.EXECUTOR_PERSONS, userRegistrationData);
    return response.data.details
}

export async function createDocumentTemplate(templateCreationData: DataValue[]): Promise<any>
{
    const response = await api.post(ENDPOINTS.TEMPLATES, templateCreationData,
        { headers: { "Content-Type": "multipart/form-data" }
    });
    if (response.status !== 201) throw new Error(response.data.details);
    return response.data.details
}

function objectToFormData(obj: any, form?: FormData, namespace?: string): FormData {
    const fd = form || new FormData();

    for (const property in obj) {
        if (!obj.hasOwnProperty(property) || obj[property] === undefined) continue;

        const formKey = namespace ? `${namespace}[${property}]` : property;
        const value = obj[property];

        if (value instanceof Date) {
            fd.append(formKey, value.toISOString());
        } else if (value instanceof File || value instanceof Blob) {
            fd.append(formKey, value);
        } else if (Array.isArray(value)) {
            value.forEach((element, index) => {
                const arrayKey = `${formKey}[${index}]`;
                if (typeof element === 'object' && element !== null) {
                    objectToFormData(element, fd, arrayKey);
                } else {
                    fd.append(arrayKey, element);
                }
            });
        } else if (typeof value === 'object' && value !== null) {
            objectToFormData(value, fd, formKey);
        } else {
            fd.append(formKey, value);
        }
    }

    return fd;
}

export async function login(userLoginData: DataValue[]): Promise<User>
{
    const response = await api.post<DataValue[], ApiResponse<User>>(ENDPOINTS.LOGIN, userLoginData);
    if (!response.details) throw new Error("Не удалось выполнить логин");
    return response.details;
}

export async function logout()
{
    return await api.post<void, ApiResponse<string>>(ENDPOINTS.LOGOUT);
}

export async function getUser(): Promise<User>
{
    const response = await api.get<ApiResponse<User>>(ENDPOINTS.CHECK_AUTH);
    return response.data.details as User;
}

async function getFields(URL: string): Promise<Field[]>
{
    return (await api.get<Field[]>(URL)).data;
}

async function getCsrfToken(): Promise<string>
{
    const response = await api.get<ApiResponse<string>>(ENDPOINTS.CSRF);
    const token = response.data.details;
    if (!token) throw new Error("Не удалось получить CSRF-токен");
    return token;
}