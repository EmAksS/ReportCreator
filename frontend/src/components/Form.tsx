import Input, {InputProps} from "./Input";
import Button, {ButtonType} from "./Button";
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
        const newFields: InputPresentation[] = []

        props.inputs.forEach((input) =>
        {
            newFields.push({field: input.inputData, value: {fieldId: input.inputData.keyName}} as InputPresentation)
        })

        setFields(newFields);
    }, [props.inputs]);

    useEffect(() =>
    {
        const message = props.alertMessage ? props.alertMessage : "";
        setAlertMessage("form", message)
    }, [props.alertMessage]);

    const onInputChange = (key: string, newValue: FieldValue) =>
    {
        console.log(fields);
        const newFields = [...fields];
        console.log(newFields);

        const changedFieldIndex: number = newFields.findIndex((field) => field.field.keyName === key);
        console.log(changedFieldIndex);
        newFields[changedFieldIndex].value.value = newValue;
        console.log(newValue);

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
            <Button text={"fa"} variant={ButtonType.general} onClick={() => props.onSubmit(fields)}/>
        </div>)
}

export default Form;