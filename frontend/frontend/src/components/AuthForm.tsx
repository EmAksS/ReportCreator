import {FC, ReactElement, useEffect, useState} from "react";
import Form from "./Form";
import Button, {ButtonType} from "./Button";
import {
    getLoginFields,
    getRegisterCompanyFields,
    requestCreateCompany,
    requestCreateUser,
    requestLogin
} from "../api/api";
import {DataValue, Field} from "../types/api";

export enum AuthFormMode
{
    login,
    registration,
}

export interface AuthFormProps
{
    mode: AuthFormMode
}

const AuthForm: FC<AuthFormProps> = ({mode}) =>
{
    const [menuMode, setMenuMode] = useState<AuthFormMode>(mode);
    const [registerCompanyFields, setRegisterCompanyFields] = useState<Field[]>([]);
    const [loginFields, setLoginFields] = useState<Field[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [alertMessage, setAlertMessage] = useState<string>("");

    useEffect(() =>
    {
        requestAndLoadFields();
    }, []);

    const requestAndLoadFields = async () =>
    {
        try
        {
            const fetchedLoginFields = await getLoginFields();
            setLoginFields(fetchedLoginFields);
            const fetchedRegisterCompanyFields = await getRegisterCompanyFields();
            setRegisterCompanyFields(fetchedRegisterCompanyFields);
        }
        catch (error)
        {
            console.error('Failed to load form fields:', error);
            setAlertMessage('Не удалось загрузить форму');
        }
        finally
        {
            setLoading(false);
        }
    };

    const sendCompanyCreateRequest = (fields: Field[], values: Record<string, string | boolean>)=>
    {
        try
        {
            const dataValues: DataValue[] = getDataValueArray(fields, values);
            requestCreateCompany(dataValues)
        }
        catch (error)
        {
            if (error instanceof Error) setAlertMessage(error.message)
        }
    }

    const sendLoginRequest = (fields: Field[], values: Record<string, string | boolean>)=>
    {
        try
        {
            const dataValues: DataValue[] = getDataValueArray(fields, values);
            requestLogin(dataValues)
        }
        catch (error)
        {
            if (error instanceof Error) setAlertMessage(error.message)
        }

    }

    const getDataValueArray = (fields: Field[], values: Record<string, string | boolean>): DataValue[] =>
    {
        const dataValues: DataValue[] = [];

        for (let i = 0; i < fields.length; i++)
        {
            const field = fields[i];
            const value = values[field.keyName]
            if (field.isRequired && !value)
            {
                throw Error(`Поле "${field.name}" должно быть заполнено`)
            }
            dataValues.push({fieldId: field.keyName, fieldValue: value})
        }

        return dataValues
    }

    const getForm = (): ReactElement =>
    {
        switch (menuMode)
        {
            case AuthFormMode.login:
                return <Form
                    style={{width: "400px"}}
                    inputs={loginFields.map((field) => {
                        return {inputData: field}
                    })}
                    onSubmit={sendLoginRequest}
                    buttons={[{
                        type: "submit",
                        text: "Войти",
                        onClick: ()=>{},
                        style: {width: "100%", marginTop: "18px"},
                        variant: ButtonType.general}]}/>;

            case AuthFormMode.registration:
                return <Form
                    style={{width: "400px"}}
                    inputs={[...registerCompanyFields, ...loginFields].map((field) =>
                    {
                        return {inputData: field}
                    })}
                    onSubmit={sendCompanyCreateRequest}
                    alertMessage={alertMessage}
                    buttons={[{
                        type: "submit",
                        text: "Зарегистрировать компанию",
                        onClick: ()=>{},
                        style: {width: "100%", marginTop: "18px"},
                        variant: ButtonType.general}]}></Form>;
        }
    }

    return (
        <div className={"authorization-form"}>
            <div style={{display: "flex", flexDirection: "row", justifyContent: "space-around"}}>
                <Button style={{width: "45%"}}
                        text={"Вход"}
                        onClick={() => setMenuMode(AuthFormMode.login)}
                        variant={ButtonType.toggleable}/>
                <Button style={{width: "45%"}}
                        text={"Регистрация компании"}
                        onClick={() => setMenuMode(AuthFormMode.registration)}
                        variant={ButtonType.toggleable}/>
            </div>
            {loading ? <div>Загрузка</div> : getForm()}
        </div>
    )
}

export default AuthForm;