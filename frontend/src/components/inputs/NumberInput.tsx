import {FC} from "react";
import TextInput, {TextInputProps} from "./TextInput";

export interface NumberInputProps extends TextInputProps { }

const NumberInput: FC<NumberInputProps> = (props) =>
{
    return (<TextInput {...props} inputData={{...props.inputData, validationRegex: "^\\d{1,9}$"}} />);
}

export default NumberInput;