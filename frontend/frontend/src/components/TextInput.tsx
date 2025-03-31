import {FC} from "react";

export interface TextInputProps
{
    placeholder?: string;
    secureText?: boolean;
    style?: React.CSSProperties;
}

const TextInput: FC<TextInputProps> = (props: TextInputProps) =>
{
    return (<input type={"text"} className={"text-input" + (props.secureText === true ? " secure-text" : "")}
                   placeholder={props.placeholder ? props.placeholder : ""}
                   style={props.style ? props.style : {}}/>)
}

export default TextInput;