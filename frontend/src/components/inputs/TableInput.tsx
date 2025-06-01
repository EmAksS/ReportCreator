// src/components/inputs/TableInput.tsx
import { FC, ReactElement, useEffect, useState } from "react";
import { FieldValue, InputPresentation, TableField } from "../../types/api";
import Input from "../Input";
import List, { ListItem } from "../List";

// Забираем всё из InputProps, кроме onChange
type BaseInputProps = Omit<import("../Input").InputProps, "onChange">;

export interface TableInputProps extends BaseInputProps {
    tableFields: TableField[];
    // Теперь onChange отдаёт сразу всю “матрицу” строк
    onChange?: (keyName: string, rows: FieldValue[][]) => void;
}

interface TableRow {
    id: number;
    inputs: InputPresentation[];
}

const TableInput: FC<TableInputProps> = (props: TableInputProps) => {
    const [rows, setRows] = useState<TableRow[]>([]);

    // При монтировании добавляем одну пустую строку
    useEffect(() => {
        addEmptyRow();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    // Добавление новой пустой строки
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

    // Ищем первый свободный id
    const getFreeId = (rowsArray: TableRow[]): number => {
        const usedIds = new Set(rowsArray.map((r) => r.id));
        let i = 0;
        while (usedIds.has(i)) i++;
        return i;
    };

    // Собираем “матрицу” значений из rows
    const getMatrix = (rowsArray: TableRow[]): FieldValue[][] =>
        rowsArray.map((row) => row.inputs.map((cell) => cell.value.value));

    // Обработчик, когда изменилась одна ячейка таблицы
    // rowId — id строки, columnKeyName — keyName столбца, newValue — введённое значение
    const onCellChange = (
        rowId: number,
        columnKeyName: string,
        newValue: FieldValue
    ) => {
        setRows((prevRows) => {
            const newRows = prevRows.map((row) => {
                if (row.id !== rowId) return row;

                // Обновляем только ту ячейку, где keyName === columnKeyName
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

            // Посылаем наверх новую матрицу
            const matrix = getMatrix(newRows);
            props.onChange?.(props.inputData.keyName, matrix);
            return newRows;
        });
    };

    // Удаление строки (минимум одна остаётся)
    const removeRowById = (idToRemove: number) => {
        setRows((prevRows) => {
            if (prevRows.length < 2) return prevRows;
            const filtered = prevRows.filter((r) => r.id !== idToRemove);
            const matrix = getMatrix(filtered);
            props.onChange?.(props.inputData.keyName, matrix);
            return filtered;
        });
    };

    // Шапка таблицы (названия столбцов)
    const renderHeader = (): ReactElement => (
        <div className="table-row table-header">
            {props.tableFields.map((field) => (
                <div className="table-cell" key={"th-" + field.keyName}>
                    {field.name}
                </div>
            ))}
        </div>
    );

    // Содержание списка строк: в каждой ячейке — <Input>
    // Теперь onChange у Input принимает (keyName, value) и мы их передаём в onCellChange
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
