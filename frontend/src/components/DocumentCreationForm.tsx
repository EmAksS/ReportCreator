import React, {ChangeEvent, FC, useEffect, useState} from "react";
import {DataValue, Field} from "../types/api";
import {
    createDocument,
    createDocumentTemplate,
    createTemplateField,
    getCompany,
    getCompanyDocumentTemplates,
    getDocumentFields,
    getTemplateFieldsFields
} from "../api/api";
import {DocumentTemplate} from "../types/core";
import Form from "./Form";
import {InputProps} from "./Input";

const DocumentCreationForm: FC = () =>
{
    const [templates, setTemplates] = useState<DocumentTemplate[]>([])
    const [selectedTemplateId, setSelectedTemplateId] = useState<string>("")
    const [selectedTemplateFieldFields, setSelectedTemplateFieldFields] = useState<Field[]>([])
    const [fields, setFields] = useState<Field[]>()

    useEffect(() =>
    {
        requestTemplates()
    }, []);

    useEffect(() =>
    {
        requestFieldsFields()
    }, [selectedTemplateId])

    const requestTemplates = async () =>
    {
        const company = await getCompany();
        const requestedTemplates = await getCompanyDocumentTemplates(company.id);
        console.log(requestedTemplates);
        setTemplates(requestedTemplates);
    }

    const requestFieldsFields = async () =>
    {
        const requestedFields = await getTemplateFieldsFields(Number(selectedTemplateId));
        console.log(requestedFields);
        setSelectedTemplateFieldFields(requestedFields);
    }

    const handleTemplateSelect = async (event: ChangeEvent<HTMLSelectElement>) =>
    {
        const selectedTemplateId = event.target.value;
        setSelectedTemplateId(selectedTemplateId);
        const selectedDocumentTemplateFields = await getDocumentFields(Number(selectedTemplateId))
        setFields(selectedDocumentTemplateFields);
    }

    const onTemplateFieldCreate = async (values: DataValue[]) =>
    {
        const response = await createTemplateField(Number(selectedTemplateId), values);
    }

    return <div>
        <p style={{margin: "14px auto"}}>Шаблон документа</p>
        <select onChange={handleTemplateSelect} className={"text-input combobox-input"} value={selectedTemplateId}>
            <option value="" disabled hidden>Выберите значение</option>
            {templates ? templates.map(template => <option key={template.id} value={template.id}>{template.templateType + ": " + template.templateName}</option>) : null}
        </select>

        {fields ? <Form key={selectedTemplateId} submitLabel={"Создать документ"}
                        inputs={fields.map(field => ({inputData: field} as InputProps))}
                        onSubmit={(values) => createDocument(Number(selectedTemplateId), values)}></Form> : null}
    </div>
}

export default DocumentCreationForm;
