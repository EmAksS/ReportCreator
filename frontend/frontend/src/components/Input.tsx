import {FC, ReactElement, useEffect, useState} from "react";
import {Field, InputPresentation, InputType} from "../types/api";

export interface InputProps
{
    inputData: Field;
    onChange?: React.ChangeEventHandler<HTMLInputElement>;
    alert?: (keyName: string, message: string) => void;
    style?: React.CSSProperties;
}

const Input: FC<InputProps> = (props: InputProps) =>
{
    const [inputPresentation, setInputPresentation] = useState<InputPresentation>();

    useEffect(() =>
    {
        setInputPresentation({
                field: props.inputData,
                value: {fieldId: props.inputData.keyName, fieldValue: ""}})
    }, []);

    useEffect(() =>
    {
        setValidationRegex(RegExp(props.inputData.validationRegex as string));
    }, [props.inputData.validationRegex])

    const onInputChange = (event: React.ChangeEvent<HTMLInputElement>): void =>
    {
        updateAlertMessage(event.target.value);
        props.onChange?.(event);
    }

    const updateAlertMessage = (value: string): void =>
    {
        if (!props.alert) return;

        const passedValidation: boolean = validateValue(value)

        let alertMessage: string = (value !== "" && !passedValidation)
            ? props.inputData.errorText || `Неверный формат значения в поле "${props.inputData.name}"`
            : "";

        props.alert(props.inputData.keyName, alertMessage);
    }
    
    const validateValue = (value: string): boolean =>
    {
        return props.inputData.type === InputType.Checkbox
            || (validationRegex ? validationRegex.test(value) : true);
    }

    const getInputTag = (): ReactElement =>
    {
        const inputData = props.inputData;

        switch (inputData.type)
        {
            case InputType.Text:
            {
                return (<input type={"text"}
                               className={"text-input " + (inputData.secureText ? "secure-text" : "")}
                               placeholder={inputData.placeholder}
                               style={props.style}
                               onChange={onInputChange}/>)
            }
            case InputType.Table:
            {
                return (<div>eto tablitsa</div>)
            }
            case InputType.Checkbox:
            {
                return (<input type={"checkbox"} onChange={props.onChange}/>)
            }
            default: return (<div>Not valid input type</div>);
        }
    }

    return getInputTag();
}

export default Input;