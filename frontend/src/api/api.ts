import axios from "axios";
import camelcaseKeys from 'camelcase-keys';
import snakecaseKeys from "snakecase-keys";
import {ApiResponse, CsrfToken, DataValue, Field, IsAuthenticatedApiResponse} from "../types/api";

const BASE_API_URL = "http://localhost:8000";
const ENDPOINTS = {
    CHECK_AUTH: "/check_auth/",
    USER_REGISTRATION_FIELDS: "/user/values/fields/",
    COMPANY_REGISTRATION: "/register/company/",
    CREATE_USER: "/register/user/",
    CREATE_COMPANY: "/register/company/",
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
        config.data = camelToSnake(data);
    }
    return config;
});

api.interceptors.request.use(async (config) =>
{
    if (config.url && config.url !== ENDPOINTS.CSRF)
    {
        const token = await getCsrfToken();
        console.log("токен" + token);
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
            response.data = snakeToCamel(data);
        }
        return response;
    },
    (error) =>
    {
        console.error(error);
        return Promise.reject(error);
    });

function snakeToCamel(data: any): any
{
    return camelcaseKeys(data, { deep: true });
}

function camelToSnake(data: any): any
{
    return snakecaseKeys(data, { deep: true });
}

export async function isAuthenticated(): Promise<boolean>
{
    return (await api.get<IsAuthenticatedApiResponse>(ENDPOINTS.CHECK_AUTH)).data.status == 200;
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
    const data = response.data;
    console.log(data);
    return data;
}

export async function requestCreateUser(userRegistrationData: DataValue[]): Promise<void>
{
    await postDataValue(ENDPOINTS.CREATE_USER, userRegistrationData)
}

export async function requestCreateCompany(companyRegistrationData: DataValue[])
{
    const response = await postDataValue<IsAuthenticatedApiResponse>(ENDPOINTS.COMPANY_REGISTRATION, companyRegistrationData);
    console.log("отпрвляем запрос регистрации компании " + companyRegistrationData);
    if (!response.user) throw new Error(response.details);
    return response
}

export async function requestLogin(userLoginData: DataValue[])
{
    const response = await postDataValue<IsAuthenticatedApiResponse>(ENDPOINTS.LOGIN, userLoginData);
    console.log("отпрвляем запрос логина " + userLoginData);
    if (!response.user) throw new Error(response.details);
    return response
}

export async function requestLogout()
{
    const response = await api.post<void, void>(ENDPOINTS.LOGOUT);
    console.log("отправляем запрос logout");
}

async function postDataValue<TResponseValue>(URL: string, data: DataValue[]): Promise<TResponseValue>
{
    return (await api.post<DataValue[]>(URL, { data: data })).data as TResponseValue;
}

async function getCsrfToken(): Promise<string>
{
    const response = await api.get<ApiResponse>(ENDPOINTS.CSRF);
    const token = response.data.details;
    if (!token) throw new Error("Не удалось получить CSRF-токен");
    return token;
}