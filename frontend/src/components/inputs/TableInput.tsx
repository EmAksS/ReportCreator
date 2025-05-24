import { FC, ReactElement, useEffect, useState } from "react";
import { FieldValue, InputPresentation, TableField } from "../../types/api";
import Input, { InputProps } from "../Input";
import List, { ListItem } from "../List";

export interface TableInputProps extends InputProps {
    inputData: TableField;
}

interface TableRow {
    id: number;
    inputs: InputPresentation[];
}

const TableInput: FC<TableInputProps> = (props: TableInputProps) => {
    const [rows, setRows] = useState<TableRow[]>([]);

    useEffect(() => {
        addEmptyRow();
    }, []);

    const addEmptyRow = () => {
        setRows(prevRows => {
            const emptyRow: TableRow = {
                id: getFreeId(prevRows),
                inputs: props.inputData.fields.map(field => ({
                    field,
                    value: {
                        fieldId: `${field.keyName}__${props.inputData.relatedTable}`,
                        value: ""
                    }
                }))
            };
            return [...prevRows, emptyRow];
        });
    };

    const getFreeId = (rowsArray: TableRow[]): number => {
        const usedIds = new Set(rowsArray.map(row => row.id));
        let i = 0;
        while (usedIds.has(i)) i++;
        return i;
    };

    const onInputChange = (keyName: string, newValue: FieldValue) => {
        setRows(prevRows => {
            const newRows = prevRows.map(row => {
                const newInputs = row.inputs.map(input => {
                    if (input.field.keyName === keyName) {
                        return {
                            ...input,
                            value: { ...input.value, value: newValue }
                        };
                    }
                    return input;
                });
                return { ...row, inputs: newInputs };
            });
            // Передаём изменённое значение во внешний обработчик, если он указан
            props.onChange?.(props.inputData.keyName, getFieldValue(newRows));
            return newRows;
        });
    };

    const getFieldValue = (rowsArray: TableRow[]): FieldValue => {
        return rowsArray.map(row => row.inputs.map(cell => cell.value.value));
    };

    const removeRowById = (idToRemove: number) => {
        setRows(prevRows => {
            if (prevRows.length < 2) return prevRows;
            const updatedRows = prevRows.filter(row => row.id !== idToRemove);
            props.onChange?.(props.inputData.keyName, getFieldValue(updatedRows));
            return updatedRows;
        });
    };

    const getTableHeader = (): ReactElement => {
        return (
            <div className="table-row table-header">
                {props.inputData.fields.map(field => (
                    <div className="table-cell" key={"table-header-cell" + field.keyName}>
                        {field.name}
                    </div>
                ))}
            </div>
        );
    };

    const listItems: ListItem[] = rows.map(row => ({
        id: row.id,
        content: (
            <div className="table-row">
                {row.inputs.map(input => (
                    <div className="table-cell" key={`${row.id}_${input.field.keyName}`}>
                        <Input inputData={input.field} onChange={onInputChange} />
                    </div>
                ))}
            </div>
        )
    }));

    return (
        <div className="form-item table-input">
            {getTableHeader()}
            <List items={listItems} onAdd={addEmptyRow} onRemove={removeRowById} />
        </div>
    );
};

export default TableInput;
