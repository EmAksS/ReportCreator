import {FC, useEffect, useState} from "react";
import {FieldValue, TextField} from "../../types/api";
import {InputProps} from "../Input";

export interface TextInputProps extends InputProps
{
    inputData: TextField;
}

const TextInput: FC<TextInputProps> = (props: TextInputProps) =>
{
    const [validationRegExp, setValidationRegExp] = useState<RegExp>();

    useEffect(() => {
        setValidationRegExp(new RegExp(props.inputData.validationRegex as string));
    }, [props.inputData.validationRegex]);


    const handleChange = (event: React.ChangeEvent<HTMLInputElement>): void =>
    {
        const newValue: FieldValue = event.target.value
        updateAlertMessage(newValue);
        props.onChange?.(props.inputData.keyName, newValue);
    };

    const updateAlertMessage = (value: string): void =>
    {
        if (!props.alert) return;

        const isValid: boolean = validateValue(value)

        let alertMessage: string = (!isValid && value !== "")
            ? props.inputData.errorText || `Неверный формат значения в поле "${props.inputData.name}"`
            : "";

        props.alert(props.inputData.keyName, alertMessage);
    }

    const validateValue = (value: string): boolean =>
    {
        return validationRegExp ? validationRegExp.test(value) : true;
    }

    return (
        <input type={"text"}
               className={"form-item text-input" + (props.inputData.secureText ? " secure-text" : "")}
               placeholder={props.inputData.placeholder}
               style={props.style}
               onChange={handleChange}/>
    )
}

export default TextInput;