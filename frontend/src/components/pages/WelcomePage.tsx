import React, {FC, useEffect, useState} from "react";
import TableInput from "../inputs/TableInput";
import {Field, InputType, TableField, TextField} from "../../types/api";

const WelcomePage: FC = () =>
{
    const [userName, setUserName] = useState<string>("");

    useEffect(() => {

    }, []);

    const userPermissionsTable: TableField = {
        keyName: "permissions",
        name: "Права доступа",
        type: InputType.Table,
        isRequired: false,
        errorText: "Необходимо заполнить хотя бы одну строку",
        relatedTable: "user_permissions",
        fields: [
            {
                keyName: "permissionName",
                name: "Название права",
                type: InputType.Text,
                isRequired: true,
                errorText: "Обязательное поле",
                placeholder: "Например: admin.access",
                validationRegex: "^[a-z.]+$"
            } as TextField,
            {
                keyName: "isEnabled",
                name: "Активно",
                type: InputType.Checkbox,
                isRequired: false,
                errorText: null
            } as Field,
            {
                keyName: "documentRef",
                name: "Ссылка на документ",
                type: InputType.Text,
                isRequired: false,
                errorText: "Некорректный формат ссылки",
                placeholder: "DOC-0000",
            } as TextField,
            {
                keyName: "expiryDate",
                name: "Срок действия",
                type: InputType.Text,
                isRequired: true,
                errorText: "Укажите дату в формате ДД.ММ.ГГГГ",
                placeholder: "ДД.ММ.ГГГГ",
                validationRegex: "^\\d{2}\\.\\d{2}\\.\\d{4}$",
                secureText: true // Показывать звездочками при вводе
            } as TextField,
        ]
    };

    return (<div style={{padding: "100px"}}><TableInput inputData={userPermissionsTable}/></div>)
}

export default WelcomePage;
