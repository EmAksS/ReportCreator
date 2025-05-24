import {FC, ReactElement} from "react";
import {Field, FieldValue, InputType} from "../types/api";
import TextInput, {TextInputProps} from "./inputs/TextInput";
import TableInput, {TableInputProps} from "./inputs/TableInput";
import CheckboxInput from "./inputs/CheckboxInput";
import ComboboxInput, {ComboboxInputProps} from "./inputs/ComboboxInput";
import FileInput, {FileInputProps} from "./inputs/FileInput";

export interface InputProps
{
    inputData: Field;
    onChange?: (keyName: string, value: FieldValue) => void;
    alert?: (keyName: string, message: string) => void;
    style?: React.CSSProperties;
    canPassDefaultValue?: boolean;
}

const Input: FC<InputProps> = (props: InputProps) =>
{
    const getInputTag = (): ReactElement =>
    {
        const inputData = props.inputData;

        switch (inputData.type)
        {
            case InputType.Text: return <TextInput {...props as TextInputProps} />

            case InputType.Table: return <TableInput {...props as TableInputProps} />

            case InputType.Checkbox: return <CheckboxInput {...props} />

            case InputType.Combobox: return <ComboboxInput {...props as ComboboxInputProps} />

            case InputType.File: return <FileInput {...props as FileInputProps} />

            default: throw new Error("Предоставлен не валидный объект Field")
        }
    }

    return getInputTag();
}

export default Input;