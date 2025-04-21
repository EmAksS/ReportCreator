import axios, {AxiosError} from "axios";
import camelcaseKeys from 'camelcase-keys';
import snakecaseKeys from "snakecase-keys";
import {DataValue, Field} from "../types/api";

const BASE_API_URL = "http://26.213.134.143:8000";
const LOGIN_FIELDS_URL = "/login/fields";
const USER_REGISTRATION_FIELDS_URL = "/user/values/fields/";
const COMPANY_REGISTRATION_FIELDS_URL = "/company/fields/";
const CREATE_USER_URL = "/register/user/";
const CREATE_COMPANY_URL = "/register/company/";
const LOGIN_URL = "/login/";

axios.defaults.baseURL = BASE_API_URL;
axios.defaults.withCredentials = true;


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
        const response = await axios.get(URL, {transformResponse: [snakeToCamel]});
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
    try {postDataValue(CREATE_USER_URL, userRegistrationData)}
    catch (error) {console.error('Ошибка при регистрации пользователя:', error)}
}

export async function requestCreateCompany(companyRegistrationData: DataValue[]): Promise<void>
{
    try {postDataValue(CREATE_COMPANY_URL, companyRegistrationData)}
    catch (error) {console.error('Ошибка при регистрации компании:', error)}
}

export async function requestLogin(userLoginData: DataValue[]): Promise<void>
{
    try {postDataValue(LOGIN_URL, userLoginData)}
    catch (error) {console.error('Ошибка при логине:', error)}
}

async function postDataValue(URL: string, userLoginData: DataValue[])
{
    try
    {
        const response = await axios.post(URL,
            {
                data: JSON.stringify(camelToSnake(userLoginData))
            });
    }
    catch (error)
    {
        if (error instanceof AxiosError) console.log(error.response);
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
    if (typeof data === 'string') {
        try {
            data = JSON.parse(data);
        } catch {
            return data; // Если не JSON, возвращаем строку как есть
        }
    }

    // Если data — массив, обрабатываем каждый элемент рекурсивно
    if (Array.isArray(data)) {
        return data.map(item => camelToSnake(item));
    }

    // Если data — объект (и не null), применяем snakecaseKeys
    if (typeof data === 'object' && data !== null) {
        return snakecaseKeys(data, { deep: true });
    }

    // Для примитивов (числа, boolean, null, undefined) возвращаем как есть
    return data;
}