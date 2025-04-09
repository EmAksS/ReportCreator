export interface UserLoginData
{
    username: string,
    password: string
}

export interface Credentials
{
    lastName: string,
    firstName: string,
    patronymic?: string
}

export interface User extends Credentials, UserLoginData { }

export interface Executor extends User
{
    companyName: string,
    companyFullName: string,
}

export interface DataValue
{
    id: number,
    dataId: Data,
    fieldId: Field,
    value: string | TableRow[] | boolean
}

export interface Data
{
    id: number,
    data: any;
}

export interface Field
{
    name: string;
    keyName: string;
    placeholder?: string;
    validationRegEx?: RegExp;
    isRequired: boolean;
    inputType: "text" | "table" | "checkbox";
    secureText?: boolean;
}

export interface TableRow
{
    [key: string]: Field;
}

export interface CredentialsInput extends Field, Credentials { }

// interface ApiResponse<T> {
//     status: 'success' | 'error';
//     data?: T;
//     error?: string;
// }
//
// interface AuthCheckResponse {
//     status: 'authenticated' | 'not_authenticated';
//     user?: User;
// }