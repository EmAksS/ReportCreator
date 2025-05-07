import {FC, ReactElement, useEffect, useState} from "react";
import {FieldValue, InputPresentation, TableField} from "../../types/api";
import Input, {InputProps} from "../Input";

export interface TableInputProps extends InputProps
{
    inputData: TableField;
}

interface TableRow
{
    id: number
    inputs: InputPresentation[];
}

const TableInput: FC<TableInputProps> = (props: TableInputProps) => {
    const [rows, setRows] = useState<TableRow[]>([]);

    useEffect(() =>
    {
        addEmptyRow();
    }, []);

    const addEmptyRow = () =>
    {
        const newRows = [...rows];

        const emptyRow: TableRow = {
            id: getFreeId(),
            inputs: props.inputData.fields.map((field): InputPresentation => {
                return {
                    field: field,
                    value: {fieldId: `${field.keyName}__${props.inputData.relatedTable}`, value: ""}
                }
            })
        }
        newRows.push(emptyRow);
        setRows(newRows);
    }

    const getFreeId = (): number =>
    {
        const usedIds = new Set(rows.map(row => row.id));
        let i = 0;
        while (usedIds.has(i)) i++
        return i;
    }

    const getTable = (): ReactElement =>
    {
        return (
            <div className={"form-item table-input"}>
                {getTableHeader()}

                {rows.map((row) =>
                {
                    return (<div className={"table-row"} key={row.id}>
                        {row.inputs.map((input) =>
                        {
                            return (<div className={"table-cell"} key={row.id + input.field.keyName}>
                                <Input inputData={input.field} onChange={onInputChange}/>
                            </div>)
                        })}

                        <button className={"table-row-remove-button"} onClick={() => removeRowById(row.id)}>-</button>
                    </div>)})
                }

                <button className={"table-row-add-button"} onClick={() => addEmptyRow()}>+</button>
            </div>
        )
    }

    const getTableHeader = (): ReactElement =>
    {
        return (
            <div className={"table-row"}>
                {props.inputData.fields.map((field) =>
                {
                    return <div className={"table-cell"} key={"table-header-cell" + field.keyName}>{field.name}</div>
                })}
            </div>);
    }

    const onInputChange = (keyName: string, newValue: FieldValue) =>
    {
        const newRows = [...rows];

        newRows.forEach((row) =>
        {
            row.inputs.forEach((input) =>
            {
                if (input.field.keyName == keyName)
                {
                    input.value.value = newValue;
                }
            })
        });

        setRows(newRows);

        props.onChange?.(props.inputData.keyName, getFieldValue())
    }

    const getFieldValue = (): FieldValue =>
    {
        return rows.map(row => row.inputs.map(cell => cell.value.value))
    }

    const removeRowById = (idToRemove: number) =>
    {
        if (rows.length < 2) return;
        setRows(rows.filter(row => row.id !== idToRemove));
    }

    return getTable();
}
export default TableInput;