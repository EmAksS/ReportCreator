import {FC, ReactElement} from "react";
import {Field} from "../types/types";

export interface InputProps
{
    inputData: Field;
    onChange?: React.ChangeEventHandler<HTMLInputElement>;
    alert?: (keyName: string, message: string) => void;
    style?: React.CSSProperties;
}

const Input: FC<InputProps> = (props: InputProps) =>
{
    const onInputChange = (event: React.ChangeEvent<HTMLInputElement>): void =>
    {
        const passedValidation = validateValue(event.target.value);

        const alertMessage = passedValidation ? "" : "Неверный формат значения в поле '" + props.inputData.name + "'";
        props.alert?.(props.inputData.keyName, alertMessage);

        props.onChange?.(event);
    }
    
    const validateValue = (value: string): boolean =>
    {
        return props.inputData.validationRegEx?.test(value) || value === "";
    }

    const getInputTag = (): ReactElement =>
    {
        const inputData = props.inputData;

        switch (inputData.inputType)
        {
            case "text":
            {
                return (<input type={"text"}
                               className={"text-input " + (inputData.secureText ? "secure-text" : "")}
                               placeholder={inputData.placeholder}
                               style={props.style}
                               onChange={onInputChange}/>)
            }
            case "table":
            {
                return (<div>eto tablitsa</div>)
            }
            case "checkbox":
            {
                return (<input type={"checkbox"} onChange={props.onChange}/>)
            }
            default: return (<div>Not valid input type</div>);
        }
    }

    return getInputTag();
}

export default Input;