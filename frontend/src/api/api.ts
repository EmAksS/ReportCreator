import axios from "axios";
import camelcaseKeys from 'camelcase-keys';
import snakecaseKeys from "snakecase-keys";
import {ApiResponse, DataValue, Field} from "../types/api";
import {User} from "../types/core";

const BASE_API_URL = "http://localhost:8000";
const ENDPOINTS = {
    CHECK_AUTH: "/check_auth/",
    USER_REGISTRATION_FIELDS: "/user/values/fields/",
    COMPANY_REGISTRATION: "/register/company/",
    USER_REGISTRATION: "/register/user/",
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
    if (data)
    {
        config.data = toSnake(data);
    }
    return config;
});

api.interceptors.request.use(async (config) =>
{
    if (config.url && config.url !== ENDPOINTS.CSRF)
    {
        const token = await getCsrfToken();
        config.headers["X-CSRFToken"] = token;
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

function toCamel(data: any): any
{
    return camelcaseKeys(data, { deep: true });
}

function toSnake(data: any): any
{
    return snakecaseKeys(data, { deep: true });
}

export async function isAuthenticated(): Promise<boolean>
{
    const response = await api.get<ApiResponse<User>>(ENDPOINTS.CHECK_AUTH);
    const user = response.data.details;
    return !(!user);
}

export async function getLoginFields(): Promise<Field[]>
{
    return await getFields(ENDPOINTS.LOGIN);
}

export async function getRegisterCompanyFields(): Promise<Field[]>
{
    return await getFields(ENDPOINTS.COMPANY_REGISTRATION);
}

export async function getRegisterUserFields(): Promise<Field[]>
{
    return await getFields(ENDPOINTS.USER_REGISTRATION_FIELDS);
}

async function getFields(URL: string): Promise<Field[]>
{
    const response = await api.get<Field[]>(URL);
    const fields = response.data;
    if (!fields) throw new Error("Не удалось запросить поля")
    return fields;
}

export async function requestCreateUser(userRegistrationData: DataValue[]): Promise<User>
{
    const response = await postDataValue<ApiResponse<User>>(ENDPOINTS.USER_REGISTRATION, userRegistrationData);
    if (!response.details) throw new Error("Не удалось зарегистрировать пользователя");
    return response.details
}

export async function requestCreateCompany(companyRegistrationData: DataValue[]): Promise<User>
{
    const response = await postDataValue<ApiResponse<User>>(ENDPOINTS.COMPANY_REGISTRATION, companyRegistrationData);
    if (!response.details) throw new Error("Не удалось зарегистрировать компанию");
    return response.details
}

export async function requestLogin(userLoginData: DataValue[]): Promise<User>
{
    const response = await postDataValue<ApiResponse<User>>(ENDPOINTS.LOGIN, userLoginData);
    if (!response.details) throw new Error("Не удалось выполнить логин");
    return response.details;
}

export async function requestLogout()
{
    const response = await api.post<void, ApiResponse<string>>(ENDPOINTS.LOGOUT);
    console.log("отправляем запрос logout " + response.details);
}

async function postDataValue<TResponseValue>(URL: string, data: DataValue[]): Promise<TResponseValue>
{
    return (await api.post<DataValue[]>(URL, { data: data })).data as TResponseValue;
}

async function getCsrfToken(): Promise<string>
{
    const response = await api.get<ApiResponse<string>>(ENDPOINTS.CSRF);
    const token = response.data.details;
    if (!token) throw new Error("Не удалось получить CSRF-токен");
    return token;
}