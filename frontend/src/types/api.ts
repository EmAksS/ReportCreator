import {User} from "./core";

export enum InputType
{
    Text = "TEXT",
    Bool = "BOOL",
    Table = "TABLE",
    Combobox = "COMBOBOX",
    File = "FILE",
    Number = "NUMBER",
    Date = "DATE"
}

export interface DataValue
{
    fieldId: string,
    value: FieldValue
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

export interface ComboboxField extends Field
{
    relatedInfo: {
        url: string,
        saveField: string,
        showField: string
    }
}

export interface DocumentField extends Field
{
    relatedTemplate: string;
}

export interface TableField extends Field
{
    isAutoincremental: boolean;
    isSummable: boolean;
}

export interface InputPresentation
{
    field: Field;
    value: DataValue;
}

export interface ApiResponse<T>
{
    details: null | T;
    errors: null | Record<string, string>;
}