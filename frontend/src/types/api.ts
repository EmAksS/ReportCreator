import {User} from "./core";

export interface DataValue
{
    fieldId: string,
    value: FieldValue
}

export enum InputType
{
    Text = "TEXT",
    Checkbox = "CHECKBOX",
    Table = "TABLE"
}

export type FieldValue = string | boolean | FieldValue[][] | File;

export interface Field
{
    keyName: string;
    name: string;
    type: InputType;
    isRequired: boolean;
    errorText: string | null;
}

export interface TextField extends Field
{
    placeholder?: string;
    validationRegex?: string;
    secureText?: boolean;
}

export interface FileField extends Field
{
    fileFormat: string;
}

export interface DocumentField extends TextField
{
    relatedTemplate: string;
}

export interface TableField extends Field
{
    relatedTable: string;
    fields: Field[];
}

export interface CsrfToken
{
    csrfToken: string;
}

export interface InputPresentation
{
    field: Field;
    value: DataValue;
}

export interface ApiResponse
{
    status: number;
    details?: string;
}

export interface IsAuthenticatedApiResponse extends ApiResponse
{
    user: User
}