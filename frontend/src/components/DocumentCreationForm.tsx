import React, { ChangeEvent, FC, useEffect, useState } from "react";
import {
    createDocument, downloadDocument,
    getCompany,
    getCompanyDocumentTemplates,
    getDocumentFields,
    getTemplateTableFields,
} from "../api/api";
import { DocumentTemplate } from "../types/core";
import Form from "./Form";
import { InputProps } from "./Input";
import { Field, FieldValue, DataValue, InputType } from "../types/api";
import TableInput from "./inputs/TableInput";

const DocumentCreationForm: FC = () => {
    // 1) обычные поля
    const [fields, setFields] = useState<Record<string, Field[]>>({});
    // 2) табличные столбцы
    const [tableFields, setTableFields] = useState<Record<string, Field[]>>({});
    // 3) список шаблонов
    const [templates, setTemplates] = useState<DocumentTemplate[]>([]);
    // 4) выбранный шаблон
    const [selectedTemplateId, setSelectedTemplateId] = useState<string>("");
    // 5) сюда TableInput будет отдавать FieldValue[][] (матрицу строк)
    const [tableData, setTableData] = useState<FieldValue[][]>([]);
    // 6) прокси-поле для передачи “обычных” InputProps в Form
    const [normalInputProps, setNormalInputProps] = useState<InputProps[]>([]);

    useEffect(() => {
        requestTemplates();
    }, []);

    useEffect(() => {
        if (templates.length > 0) {
            getAllFields();
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [templates]);

    const requestTemplates = async () => {
        const company = await getCompany();
        const requestedTemplates = await getCompanyDocumentTemplates(company.id);
        setTemplates(requestedTemplates);
    };

    const getAllFields = async () => {
        const newFields: Record<string, Field[]> = {};
        const newTableFields: Record<string, Field[]> = {};

        await Promise.all(
            templates.map(async (template) => {
                const idStr = String(template.id);

                // обычные поля
                const docFields = await getDocumentFields(template.id);
                newFields[idStr] = docFields;

                // табличные поля
                const tblFields = await getTemplateTableFields(template.id);
                newTableFields[idStr] = tblFields;
            })
        );

        setFields(newFields);
        setTableFields(newTableFields);
    };

    const handleTemplateSelect = (event: ChangeEvent<HTMLSelectElement>) => {
        const newId = event.target.value;
        setSelectedTemplateId(newId);

        // сбрасываем таблицу и готовим обычные поля для Form
        setTableData([]);
        const normals = fields[newId] || [];
        setNormalInputProps(normals.map((field) => ({ inputData: field } as InputProps)));
    };

    // -----------------------------------------------------------------
    // Теперь handleTableChange соответствует новой сигнатуре:
    // (keyName: string, newTableRows: FieldValue[][]) => void
    // -----------------------------------------------------------------
    const handleTableChange = (_keyName: string, newTableRows: FieldValue[][]) => {
        setTableData(newTableRows);
    };

    const tryCreateDocument = async (normalValues: DataValue[]) => {
        // normalValues: DataValue[] по обычным полям

        // вытягиваем все колонки для выбранного шаблона
        const tf = tableFields[selectedTemplateId] || [];

        // транспонируем tableData (FieldValue[][]) так, чтобы получить массив по столбцам
        const columns: FieldValue[][] = [];

        if (tableData.length > 0) {
            for (let colIdx = 0; colIdx < tf.length; colIdx++) {
                columns[colIdx] = tableData.map((row) => row[colIdx]);
            }
        }

        // формируем DataValue[] для каждой колонки
        const tableValues: DataValue[] = tf.map((colField, idx) => ({
            fieldId: colField.keyName,
            value: columns[idx] || []
        } as DataValue));

        // объединяем все значения и отправляем
        const allValues: DataValue[] = [...normalValues, ...tableValues];
        const doc = await createDocument(Number(selectedTemplateId), allValues);

        await downloadDocument(doc.id)
    };

    return (
        <div>
            <p style={{ margin: "14px auto" }}>Шаблон документа</p>

            <select
                onChange={handleTemplateSelect}
                className="text-input combobox-input"
                value={selectedTemplateId}
            >
                <option value={""} disabled hidden>
                    Выберите шаблон
                </option>
                {templates.map((template) => (
                    <option key={template.id} value={template.id}>
                        {template.templateType}: {template.templateName}
                    </option>
                ))}
            </select>

            {selectedTemplateId && normalInputProps && (
                <div>
                    {/* 1) Обычные поля (Form) */}
                    <Form
                        key={selectedTemplateId + "-form"}
                        submitLabel="Создать документ"
                        inputs={normalInputProps}
                        onSubmit={async (values: DataValue[]) => {
                            await tryCreateDocument(values);
                        }}
                    >
                        {/* 2) Табличные поля (TableInput) — только если они есть */}
                        {(tableFields[selectedTemplateId]?.length || 0) > 0 && (
                            <div style={{ marginTop: 24 }}>
                                <p>Табличные поля:</p>
                                <TableInput
                                    // передаем “фиктивный” Field, чтобы TableInput знал keyName
                                    inputData={{
                                        keyName: "table",
                                        name: "Таблица",
                                        type: InputType.Table,
                                        isRequired: false,
                                        errorText: null
                                    }}
                                    tableFields={tableFields[selectedTemplateId] as any /* сюда точно придут TableField[] */}
                                    onChange={handleTableChange}
                                />
                            </div>
                        )}
                    </Form>


                </div>
            )}
        </div>
    );
};

export default DocumentCreationForm;
