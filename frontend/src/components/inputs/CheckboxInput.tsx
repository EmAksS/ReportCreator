import {FC, useEffect} from "react";
import {FieldValue} from "../../types/api";
import {InputProps} from "../Input";

const CheckBoxInput: FC<InputProps> = (props: InputProps) =>
{
    useEffect(() => {
        props.onChange?.(props.inputData.keyName, false)
    }, []);

    const handleChange = (event: React.ChangeEvent<HTMLInputElement>): void =>
    {
        const newValue: FieldValue = event.target.checked;
        console.log(newValue)
        props.onChange?.(props.inputData.keyName, newValue);
    };

    return (<input type={"checkbox"} style={{...props.style, width: "fit-content"}} onChange={handleChange}/>);
}

export default CheckBoxInput;