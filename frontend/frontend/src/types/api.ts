export interface DataValue
{
    fieldId: string,
    fieldValue: FieldValue
}

export enum InputType
{
    Text = "TEXT",
    Checkbox = "CHECKBOX",
    Table = "TABLE"
}

export type FieldValue = string | boolean | FieldValue[][];

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