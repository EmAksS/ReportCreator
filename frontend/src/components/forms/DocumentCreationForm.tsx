import React, { ChangeEvent, FC, useEffect, useState } from "react";
import {
    createDocument, downloadDocument,
    getCompany,
    getCompanyDocumentTemplates,
    getDocumentFields,
    getTemplateTableFields,
} from "../../api/api";
import { DocumentTemplate } from "../../types/core";
import Form from "../Form";
import { InputProps } from "../Input";
import { Field, FieldValue, DataValue, InputType } from "../../types/api";
import TableInput from "../inputs/TableInput";

const DocumentCreationForm: FC = () => {
    const [fields, setFields] = useState<Record<string, Field[]>>({});
    const [tableFields, setTableFields] = useState<Record<string, Field[]>>({});
    const [templates, setTemplates] = useState<DocumentTemplate[]>([]);
    const [selectedTemplateId, setSelectedTemplateId] = useState<string>("");
    const [tableData, setTableData] = useState<FieldValue[][]>([]);
    const [normalInputProps, setNormalInputProps] = useState<InputProps[]>([]);

    useEffect(() => {
        requestTemplates();
    }, []);

    useEffect(() => {
        if (templates.length > 0) {
            getAllFields();
        }
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

                const docFields = await getDocumentFields(template.id);
                newFields[idStr] = docFields;

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

        setTableData([]);
        const normals = fields[newId] || [];
        setNormalInputProps(normals.map((field) => ({ inputData: field } as InputProps)));
    };

    const handleTableChange = (_keyName: string, newTableRows: FieldValue[][]) => {
        setTableData(newTableRows);
    };

    const tryCreateDocument = async (normalValues: DataValue[]) => {
        const tf = tableFields[selectedTemplateId] || [];

        const columns: FieldValue[][] = [];

        if (tableData.length > 0) {
            for (let colIdx = 0; colIdx < tf.length; colIdx++) {
                columns[colIdx] = tableData.map((row) => row[colIdx]);
            }
        }

        const tableValues: DataValue[] = tf.map((colField, idx) => ({
            fieldId: colField.keyName,
            value: columns[idx] || []
        } as DataValue));

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
                    <Form
                        key={selectedTemplateId + "-form"}
                        submitLabel="Создать документ"
                        inputs={normalInputProps}
                        onSubmit={async (values: DataValue[]) => {
                            await tryCreateDocument(values);
                        }}
                    >
                        {(tableFields[selectedTemplateId]?.length || 0) > 0 && (
                            <div style={{ marginTop: 24 }}>
                                <p>Табличные поля:</p>
                                <TableInput
                                    inputData={{
                                        keyName: "table",
                                        name: "Таблица",
                                        type: InputType.Table,
                                        isRequired: false,
                                        errorText: null
                                    }}
                                    tableFields={tableFields[selectedTemplateId] as any}
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
