import {FC, useEffect, useState} from "react";
import {InputPresentation, TableField} from "../types/api";
import Input, {InputProps} from "./Input";

export interface TableInputProps extends InputProps
{
    inputData: TableField;
}

const TableInput: FC<TableInputProps> = (props: TableInputProps) =>
{
    const [rows, setRows] = useState<InputPresentation[][]>([]);

    useEffect(() =>
    {
        const startRow: InputPresentation[] = props.inputData.fields.map((field): InputPresentation =>
        {
            return {
                field: field,
                value: {fieldId: `${field.keyName}__${props.inputData.relatedTable}`, fieldValue: ""}}
        })

        rows.push(startRow)
    }, []);

    return (
        <div>
            {rows.map((row, rowIndex) =>
                    (
                        <div>
                            {row.map((cell) => <Input inputData={cell.field}/>)}
                        </div>
                    ))
            }
        </div>
    )

export default TableInput;