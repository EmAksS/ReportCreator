import {FC} from "react";
import {FieldValue} from "../../types/api";
import {InputProps} from "../Input";

const CheckBoxInput: FC<InputProps> = (props: InputProps) =>
{
    const handleChange = (event: React.ChangeEvent<HTMLInputElement>): void =>
    {
        const newValue: FieldValue = event.target.checked;
        props.onChange?.(props.inputData.keyName, newValue);
    };

    return (<input type={"checkbox"} style={props.style} onChange={handleChange}/>);
}

export default CheckBoxInput;