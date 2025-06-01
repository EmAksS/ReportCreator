import {FC} from "react";
import {FileField} from "../../types/api";
import {InputProps} from "../Input";

export interface FileInputProps extends InputProps
{
    inputData: FileField;
}

const FileInput: FC<FileInputProps> = (props: FileInputProps) =>
{
    const handleChange = (event: React.ChangeEvent<HTMLInputElement>): void =>
    {
        const files = event.target.files;

        if (files && files[0])
        {
            props.onChange?.(props.inputData.keyName, files[0]);
        }
    };

    return (<input type={"file"}
                   accept={".docx"}
                   style={props.style}
                   onChange={handleChange}
                   className={"form-item text-input"} />);
}

export default FileInput;