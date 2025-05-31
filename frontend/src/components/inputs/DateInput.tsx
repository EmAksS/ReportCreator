import {FC} from "react";
import {InputProps} from "../Input";

export interface DateInputProps extends InputProps {}

const DateInput: FC<DateInputProps> = (props) =>
{
    const handleChange = (event: React.ChangeEvent<HTMLInputElement>): void =>
    {
        console.log(event.target.value)
        props.onChange?.(props.inputData.keyName, event.target.value);
    };

    return <input className={"form-item text-input"}
                  type={"date"}
                  onChange={handleChange}
                  style={props.style} />;
}

export default DateInput;