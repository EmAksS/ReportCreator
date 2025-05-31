import React, {FC, useContext, useEffect, useState} from "react";
import {DataValue, Field} from "../types/api";
import {getDocumentTemplateCreationFields, createDocumentTemplate} from "../api/api";
import Form from "./Form";
import {ModalContext} from "./contexts/ModalContextProvider";
import FieldsSettingMenu from "./forms/FieldsSettingMenu";
import SimpleContainer from "./SimpleContainer";

const TemplateCreationForm: FC = () =>
{
    const [fields, setFields] = useState<Field[]>()
    const [fieldKeyNames, setFieldKeyNames] = useState<string[]>([])
    const {setChildren, setIsOpen} = useContext(ModalContext);

    useEffect(() => {
        getFields()
    }, []);

    const getFields = async () =>
    {
        const fields = await getDocumentTemplateCreationFields()
        setFields(fields)
    }

    const requestCreateDocumentTemplate = async (values: DataValue[]) =>
    {
        const template = await createDocumentTemplate(values);
        console.log(template)
        if (template)
        {
            setIsOpen(true);
            setChildren(<SimpleContainer><FieldsSettingMenu template={template} /></SimpleContainer>)
        }
    }

    return <div>
        {fields && fields.length > 0 ? <Form
            submitLabel={"Создать шаблон документа"}
            inputs={fields.map(field => ({inputData: field}))}
            onSubmit={requestCreateDocumentTemplate}></Form>
            : <div>Загрузка</div>}
    </div>
}

export default TemplateCreationForm;
