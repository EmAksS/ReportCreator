import Input, {InputProps} from "./Input";
import Button, {ButtonType} from "./Button";
import React, {FC, useState} from "react";
import {DataValue, Field, FieldValue, InputPresentation} from "../types/api";

export interface FormProps
{
    inputs: InputProps[];
    onSubmit: (fields: DataValue[]) => void;
    submitLabel: string;
    successfulSubmitText?: string;
    style?: React.CSSProperties;
    children?: React.ReactNode;
}

const Form: FC<FormProps> = (props: FormProps) =>
{
    const [inputs, setInputs] = useState<InputPresentation[]>(props.inputs.map(input => {
        return {field: input.inputData, value: {fieldId: input.inputData.keyName}} as InputPresentation;}));

    const [alertMessages, setAlertMessages] = useState<Record<string, string>>({});
    const [submitResultMessage, setSubmitResultMessage] = useState<string>("");

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

            if (value.value === undefined || value.value === null)
            {
                if (!field.isRequired) input.value.value = "";
                else throw Error(`Поле "${field.name}" должно быть заполнено`)
            }

            return {fieldId: value.fieldId, value: value.value} as DataValue
        })
    }

    const tryToSubmit = async () =>
    {
        try
        {
            console.log(inputs)
            const emptyFields = getEmptyRequiredFields(inputs)
            console.log(emptyFields)
            if (emptyFields.length === 0)
            {
                if (Object.keys(alertMessages).length === 0)
                {
                    await props.onSubmit(InputPresentationToDataValue())
                }
            }
            else throw Error("Все необходимые поля должны быть заполнены")
        }
        catch (e)
        {
            console.log("поймана ошибка ", e)
            if (e instanceof Error) {
                setSubmitResultMessage(e.message);
            }
            return;
        }
        setSubmitResultMessage(props.successfulSubmitText ?? "Операция выполнена успешно");
    }

    const getEmptyRequiredFields = (inputs: InputPresentation[]): Field[] =>
    {
        return inputs
            .filter((element) =>
            {
                const fieldValue = element.value.value;
                const field = element.field;

                return (fieldValue === undefined || fieldValue === null || fieldValue === "") && field.isRequired
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
            {props.children}

            <p style={{margin: "8px 0"}} className={"alert-message"}>{getFirstAlertMessage()}</p>
            <Button text={props.submitLabel} variant={ButtonType.general} onClick={tryToSubmit} style={{width: "100%"}}/>
            <p style={{margin: "8px 0", color: "black"}} className={"alert-message"}>{submitResultMessage}</p>
        </div>)
}

export default Form;