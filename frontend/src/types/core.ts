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

export interface User
{
    username: string,
    isCompanySuperuser: boolean,
}

export interface Person extends Credentials
{
    post: string
}

export interface ContractorPerson extends Person
{
    company: string
}

export interface ExecutorPerson extends Person
{

}

export interface Company
{
    companyName: string,
    companyFullName: string,
    createdAt: Date,
    updatedAt: Date
}

export interface ContractorCompany extends Company
{
    contractorCity: string,
}