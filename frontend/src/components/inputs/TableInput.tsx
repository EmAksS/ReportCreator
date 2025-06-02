import { FC, ReactElement, useEffect, useState } from "react";
import { FieldValue, InputPresentation, TableField } from "../../types/api";
import Input from "../Input";
import List, { ListItem } from "../List";

type BaseInputProps = Omit<import("../Input").InputProps, "onChange">;

export interface TableInputProps extends BaseInputProps {
    tableFields: TableField[];
    onChange?: (keyName: string, rows: FieldValue[][]) => void;
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
        setRows((prevRows) => {
            const newRowId = getFreeId(prevRows);
            const emptyRow: TableRow = {
                id: newRowId,
                inputs: props.tableFields.map((field) => ({
                    field,
                    value: {
                        fieldId: field.keyName,
                        value: "" as FieldValue
                    }
                }))
            };
            return [...prevRows, emptyRow];
        });
    };

    const getFreeId = (rowsArray: TableRow[]): number => {
        const usedIds = new Set(rowsArray.map((r) => r.id));
        let i = 0;
        while (usedIds.has(i)) i++;
        return i;
    };

    const getMatrix = (rowsArray: TableRow[]): FieldValue[][] =>
        rowsArray.map((row) => row.inputs.map((cell) => cell.value.value));

    const onCellChange = (
        rowId: number,
        columnKeyName: string,
        newValue: FieldValue
    ) => {
        setRows((prevRows) => {
            const newRows = prevRows.map((row) => {
                if (row.id !== rowId) return row;

                const updatedInputs = row.inputs.map((input) => {
                    if (input.field.keyName === columnKeyName) {
                        return {
                            ...input,
                            value: { ...input.value, value: newValue }
                        };
                    }
                    return input;
                });
                return { ...row, inputs: updatedInputs };
            });

            const matrix = getMatrix(newRows);
            props.onChange?.(props.inputData.keyName, matrix);
            return newRows;
        });
    };

    const removeRowById = (idToRemove: number) => {
        setRows((prevRows) => {
            if (prevRows.length < 2) return prevRows;
            const filtered = prevRows.filter((r) => r.id !== idToRemove);
            const matrix = getMatrix(filtered);
            props.onChange?.(props.inputData.keyName, matrix);
            return filtered;
        });
    };

    const renderHeader = (): ReactElement => (
        <div className="table-row table-header">
            {props.tableFields.map((field) => (
                <div className="table-cell" key={"th-" + field.keyName}>
                    {field.name}
                </div>
            ))}
        </div>
    );

    const listItems: ListItem[] = rows.map((row) => ({
        id: row.id,
        content: (
            <div className="table-row">
                {row.inputs.map((input) => (
                    <div className="table-cell" key={`${row.id}-${input.field.keyName}`}>
                        <Input
                            inputData={input.field}
                            onChange={(key, value) =>
                                onCellChange(row.id, key, value)
                            }
                        />
                    </div>
                ))}
            </div>
        )
    }));

    return (
        <div className="form-item table-input">
            {renderHeader()}
            <List items={listItems} onAdd={addEmptyRow} onRemove={removeRowById} />
        </div>
    );
};

export default TableInput;
