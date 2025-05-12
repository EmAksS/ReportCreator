import Input, {InputProps} from "./Input";
import Button, {ButtonProps} from "./Button";
import React, {FC, useEffect, useState} from "react";
import {FieldValue, InputPresentation} from "../types/api";

export interface FormProps
{
    inputs: InputProps[];
    onSubmit: (fields: InputPresentation[]) => void;
    alertMessage?: string;
    style?: React.CSSProperties;
    children?: React.ReactNode;
}

const Form: FC<FormProps> = (props: FormProps) =>
{
    const [fields, setFields] = useState<InputPresentation[]>([])
    const [alertMessages, setAlertMessages] = useState<Record<string, string>>({});

    useEffect(() =>
    {
        props.inputs.forEach((input) =>
        {
            fields.push({field: input.inputData, value: {fieldId: input.inputData.keyName}} as InputPresentation)
        })

    }, [props.inputs]);

    useEffect(() =>
    {
        const message = props.alertMessage ? props.alertMessage : "";
        setAlertMessage("form", message)
    }, [props.alertMessage]);

    const onInputChange = (key: string, newValue: FieldValue) =>
    {
        const newFields = [...fields];

        const changedFieldIndex: number = newFields.findIndex((field) => field.field.keyName === key);
        newFields[changedFieldIndex].value.value = newValue;

        setFields(newFields);
    };

    const setAlertMessage = (inputKeyName: string, alertMessage: string) =>
    {
        const newMessages = { ...alertMessages };

        if (alertMessage === "") delete newMessages[inputKeyName];
        else newMessages[inputKeyName] = alertMessage;

        setAlertMessages(newMessages);
    };

    const getFirstAlertMessage = (): string =>
    {
        return alertMessages[Object.keys(alertMessages)[0]];
    }

    const onSubmitButtonClick = () =>
    {
        props.onSubmit(fields);
        console.log("нажата кнопка формы")
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
                        <Input style={{width: "100%"}} alert={setAlertMessage} inputData={inputData} onChange={onInputChange} />
                    </div>)
            })}

            <p style={{margin: "8px 0"}} className={"alert-message"}>{getFirstAlertMessage()}</p>
        </div>)
}

export default Form;