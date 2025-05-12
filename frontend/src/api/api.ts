import axios, {AxiosError} from "axios";
import camelcaseKeys from 'camelcase-keys';
import snakecaseKeys from "snakecase-keys";
import {CsrfToken, DataValue, Field} from "../types/api";

const BASE_API_URL = "http://26.213.134.143:8000";
const LOGIN_FIELDS_URL = "/login/";
const USER_REGISTRATION_FIELDS_URL = "/user/values/fields/";
const COMPANY_REGISTRATION_FIELDS_URL = "/company/fields/";
const CREATE_USER_URL = "/register/user/";
const CREATE_COMPANY_URL = "/register/company/";
const LOGIN_URL = "/login/";
const CSRF_URL = "/csrf/";

const api = axios.create({
    withCredentials: true,
    baseURL: BASE_API_URL
})


export async function getLoginFields(): Promise<Field[]>
{
    return await getFields(LOGIN_FIELDS_URL);
}

export async function getRegisterCompanyFields(): Promise<Field[]>
{
    return await getFields(COMPANY_REGISTRATION_FIELDS_URL);
}

export async function getRegisterUserFields(): Promise<Field[]>
{
    return await getFields(USER_REGISTRATION_FIELDS_URL);
}

async function getFields(URL: string): Promise<Field[]>
{
    try
    {
        const response = await api.get(URL, {transformResponse: [snakeToCamel]});
        return response.data as Field[];
    }
    catch (error)
    {
        if (error instanceof AxiosError) console.log(error.response);
        throw error
    }
}

export async function requestCreateUser(userRegistrationData: DataValue[]): Promise<void>
{
    try { await postDataValue(CREATE_USER_URL, userRegistrationData)}
    catch (error) {console.error('Ошибка при регистрации пользователя:', error)}
}

export async function requestCreateCompany(companyRegistrationData: DataValue[]): Promise<void>
{
    try { await postDataValue(CREATE_COMPANY_URL, companyRegistrationData) }
    catch (error) {console.error('Ошибка при регистрации компании:', error)}
}

export async function requestLogin(userLoginData: DataValue[]): Promise<void>
{
    try { await postDataValue(LOGIN_URL, userLoginData)}
    catch (error) {console.error('Ошибка при логине:', error)}
}

async function postDataValue(URL: string, data: DataValue[])
{
    console.log("постим на " + URL + " вот это:")
    console.log(camelToSnake(data));

    try
    {
        const token = await getCsrfToken();
        console.log(token);
        const response = await api.post(URL,
            { data: camelToSnake(data), csrfmiddlewaretoken: token},
            { headers:
                    {
                        "Content-Type": "application/json",
                        "X-CSRFToken": token
                    }
            });
    }
    catch (error)
    {
        if (error instanceof AxiosError) console.log(error.response);
    }
}

async function getCsrfToken(): Promise<string>
{
    try
    {
        const response = await api.get(CSRF_URL, {transformResponse: [snakeToCamel]});
        const token = response.data as CsrfToken;
        return token.csrfToken;
    }
    catch (error)
    {
        if (error instanceof AxiosError) console.log(error.response);
        throw error
    }
}

function snakeToCamel(data: any): any
{
    try
    {
        const parsedData = JSON.parse(data);
        return camelcaseKeys(parsedData, { deep: true });
    }
    catch (error)
    {
        return data;
    }
}

function camelToSnake(data: any): any
{
    try
    {
        return snakecaseKeys(data, { deep: true });
    }
    catch (error)
    {
        return data;
    }
}