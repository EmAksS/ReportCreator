import React, {FC, useEffect, useState} from "react";
import {DataValue, Field, InputPresentation} from "../types/api";
import {getDocumentTemplateFields, createDocumentTemplate} from "../api/api";
import Form from "./Form";
import {InputProps} from "./Input";

const TemplateCreationForm: FC = () =>
{
    const [fields, setFields] = useState<Field[]>()

    useEffect(() => { getFields() }, []);

    const getFields = async () =>
    {
        const fields = await getDocumentTemplateFields()
        console.log(fields)
        setFields(fields)
    }

    const requestCreateDocumentTemplate = async (fields: DataValue[]) =>
    {
        console.log("форма просит создать шаблон", fields)
        const response = await createDocumentTemplate(fields);
        console.log(response)
    }

    return <div>
        {fields && fields.length > 0 ? <Form submitLabel={"Создать шаблон документа"} inputs={fields.map(field => ({inputData: field}))} onSubmit={requestCreateDocumentTemplate}></Form> : <div>Загрузка</div>}
    </div>
}

export default TemplateCreationForm;
