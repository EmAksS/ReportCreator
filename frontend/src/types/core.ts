export interface UserLoginData
{
    username: string,
    password: string
}

export interface Credentials
{
    lastName: string,
    firstName: string,
    surname?: string
}

export interface User extends Credentials, UserLoginData
{

}

export interface Executor extends User
{
    companyName: string,
    companyFullName: string,
}