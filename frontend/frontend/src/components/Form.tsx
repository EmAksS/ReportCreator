import Button, {ButtonProps} from "./Button";
import {FC} from "react";
import TextInput, {TextInputProps} from "./TextInput";

export interface FormProps
{
    textInputInfo: [string, TextInputProps?][];
    buttonInfo: ButtonProps[];
}

const Form: FC<FormProps> = (props: FormProps) =>
{
    return (
        <div key={"form"} className={"form"}>
            {props.textInputInfo.map((field) =>
            {
                const fieldName = field[0]
                const textInputProps = field[1]

                return (
                    <div key={fieldName}>
                        <p style={{margin:"10px 0"}}>{fieldName}</p>
                        <TextInput {...textInputProps} style={{width:"100%"}} />
                    </div>)
            })}

            {props.buttonInfo.map((buttonProps) =>
            {
                return (<Button key={buttonProps.text} {...buttonProps}/>)
            })}
        </div>)
}

export default Form;