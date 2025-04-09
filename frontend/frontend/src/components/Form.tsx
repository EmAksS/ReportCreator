import Input, {InputProps} from "./Input";
import Button, {ButtonProps} from "./Button";
import React, {FC, useEffect, useState} from "react";
import {Field} from "../types/types";

export interface FormProps
{
    inputs: InputProps[];
    buttons: ButtonProps[];
    onSubmit: (data: Field[]) => void;
    style?: React.CSSProperties;
}

const Form: FC<FormProps> = (props: FormProps) =>
{
    const [formFields, setFormFields] = useState<Field[]>([])
    const [alertMessages, setAlertMessages] = useState<Record<string, string>>({});

    useEffect(() =>
    {
        setFormFields(props.inputs.map(input => input.inputData));
    }, [props.inputs]);

    const handleInputChange = (key: string, event: React.ChangeEvent<HTMLInputElement>) =>
    {
        const newFormFields = formFields.map(item =>
        item.keyName === key ? { ...item, value: event.target.value } : item);
        setFormFields(newFormFields);
    };

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
            {props.inputs.map((inputProps) =>
            {
                const inputData = inputProps.inputData;
                return (
                    <div key={inputData.keyName}>
                        <p>{inputData.name}</p>
                        <Input style={{width: "100%"}} alert={setAlertMessage} inputData={inputData} onChange={(e) => handleInputChange(inputData.keyName, e)} />
                    </div>)
            })}

            <p className={"alert-message"}>{getFirstAlertMessage()}</p>

            <Button {...props.buttons[0]} onClick={() => props.onSubmit(formFields)} />
        </div>)
}

export default Form;