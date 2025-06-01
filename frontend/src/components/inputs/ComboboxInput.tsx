import {ChangeEvent, FC, useEffect, useState} from "react";
import {InputProps} from "../Input";
import {getComboboxItems} from "../../api/api";
import {ComboboxField} from "../../types/api";

export interface ComboboxInputProps extends InputProps
{
    inputData: ComboboxField;
}

export type ComboboxItem = Record<string, string>;

const ComboboxInput: FC<ComboboxInputProps> = (props: ComboboxInputProps) =>
{
    const [values, setValues] = useState<ComboboxItem[]>([])

    const requestComboboxValues = async () =>
    {
        const items = await getComboboxItems(props.inputData.relatedInfo.url)

        if (Array.isArray(items) && items.length > 0)
        {
            setValues(items)
            props.onChange?.(props.inputData.keyName, items[0][props.inputData.relatedInfo.saveField])
        }
    }

    useEffect(() => {
        requestComboboxValues()
    }, []);

    const handleChange = (event: ChangeEvent<HTMLSelectElement>): void =>
    {
        props.onChange?.(props.inputData.keyName, event.target.value);
    };

    return (<select
        className={"text-input combobox-input"}
        onChange={handleChange}>
        { values.map(item => <option value={item[props.inputData.relatedInfo.saveField]}>{item[props.inputData.relatedInfo.showField]}</option>) }
    </select>);
}

export default ComboboxInput;