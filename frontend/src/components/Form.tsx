import Input, {InputProps} from "./Input";
import Button, {ButtonType} from "./Button";
import React, {FC, useState} from "react";
import {DataValue, Field, FieldValue, InputPresentation} from "../types/api";

export interface FormProps
{
    inputs: InputProps[];
    onSubmit: (fields: DataValue[]) => void;
    submitLabel: string;
    style?: React.CSSProperties;
}

const Form: FC<FormProps> = (props: FormProps) =>
{
    const [inputs, setInputs] = useState<InputPresentation[]>(props.inputs.map(input => {
        return {field: input.inputData, value: {fieldId: input.inputData.keyName}} as InputPresentation;}));
    const [alertMessages, setAlertMessages] = useState<Record<string, string>>({});

    const onInputChange = (key: string, newValue: FieldValue) =>
    {
        const newFields = [...inputs];

        const changedFieldIndex: number = newFields.findIndex((field) => field.field.keyName === key);
        newFields[changedFieldIndex].value.value = newValue;

        setInputs(newFields);
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

    const InputPresentationToDataValue = (): DataValue[] =>
    {
        return inputs.map(input =>
        {
            const field = input.field
            const value = input.value

            if (!value.value)
            {
                if (!field.isRequired) input.value.value = "";
                else throw Error(`Поле "${field.name}" должно быть заполнено`)
            }

            return {fieldId: value.fieldId, value: value.value} as DataValue
        })
    }

    const tryToSubmit = () =>
    {
        if (getEmptyRequiredFields(inputs).length === 0 &&
            Object.keys(alertMessages).length === 0)
        {
            props.onSubmit(InputPresentationToDataValue())
        }
    }

    const getEmptyRequiredFields = (inputs: InputPresentation[]): Field[] =>
    {
        return inputs
            .filter((element) =>
            {
                const fieldValue = element.value.value;
                const field = element.field;

                return (!fieldValue || fieldValue === "") && field.isRequired
            })
            .map((element) => element.field)
    }

    return (
        <div className={"form"} style={props.style}>
            {!inputs ? <p>Одну секунду...</p> : inputs.map((input) =>
            {
                const field = input.field;

                return (
                    <div key={field.keyName}>
                        <p style={{margin: "8px 0"}}>{field.name + (field.isRequired ? "" : " (необязательно)")}</p>
                        <Input style={{width: "100%"}} alert={setAlertMessage} inputData={field} onChange={onInputChange} />
                    </div>)
            })}

            <p style={{margin: "8px 0"}} className={"alert-message"}>{getFirstAlertMessage()}</p>
            <Button text={props.submitLabel} variant={ButtonType.general} onClick={tryToSubmit}/>
        </div>)
}

export default Form;