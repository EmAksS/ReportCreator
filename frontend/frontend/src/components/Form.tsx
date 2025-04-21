import Input, {InputProps} from "./Input";
import Button, {ButtonProps} from "./Button";
import React, {FC, useEffect, useState} from "react";
import {Field, InputType} from "../types/api";

export interface FormProps
{
    inputs: InputProps[];
    buttons: ButtonProps[];
    onSubmit: (fields: Field[], values: Record<string, string | boolean>) => void;
    alertMessage?: string;
    style?: React.CSSProperties;
    children?: React.ReactNode;
}

const Form: FC<FormProps> = (props: FormProps) =>
{
    const [formFields, setFormFields] = useState<Field[]>([])
    const [formValues, setFormValues] = useState<Record<string, string | boolean>>({})
    const [alertMessages, setAlertMessages] = useState<Record<string, string>>({});

    useEffect(() =>
    {
        setFormFields(props.inputs.map(input => input.inputData));
    }, [props.inputs]);

    useEffect(() =>
    {
        const message = props.alertMessage ? props.alertMessage : "";
        setAlertMessage("form", message)
    }, [props.alertMessage]);

    const handleInputChange = (key: string, event: React.ChangeEvent<HTMLInputElement>) =>
    {
        const newFormFieldsValues = { ...formValues }
        const inputType = getInputPropsByKey(key)?.inputData.type;

        if (inputType === InputType.Checkbox) newFormFieldsValues[key] = event.target.checked;
        else newFormFieldsValues[key] = event.target.value;

        setFormValues(newFormFieldsValues);
    };

    const getInputPropsByKey = (key: string) =>
    {
        return props.inputs.find(input => input.inputData.keyName === key);
    }

    const setAlertMessage = (keyName: string, message: string) =>
    {
        const newAlertMessages = { ...alertMessages }

        if (message === "") delete newAlertMessages[keyName];
        else newAlertMessages[keyName] = message;

        setAlertMessages(newAlertMessages);
    };

    const getFirstAlertMessage = (): string =>
    {
        return alertMessages[Object.keys(alertMessages)[0]];
    }

    return (
        <div className={"form"} style={props.style}>
            {props.children}
            {props.inputs.map((inputProps) =>
            {
                const inputData = inputProps.inputData;
                return (
                    <div key={inputData.keyName}>
                        <p style={{margin: "8px 0"}}>{inputData.name + (inputData.isRequired ? "" : " (необязательно)")}</p>
                        <Input style={{width: "100%"}} alert={setAlertMessage} inputData={inputData} onChange={(e) => handleInputChange(inputData.keyName, e)} />
                    </div>)
            })}

            <p style={{margin: "8px 0"}} className={"alert-message"}>{getFirstAlertMessage()}</p>

            <Button {...props.buttons[0]} onClick={() => props.onSubmit(formFields, formValues)} />
        </div>)
}

export default Form;