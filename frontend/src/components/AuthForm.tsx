import React, {FC, ReactElement, useContext, useEffect, useState} from "react";
import Form from "./Form";
import Button, {ButtonType} from "./Button";
import {
    getLoginFields,
    getCompanyRegistrationFields,
    createCompany,
    login
} from "../api/api";
import {DataValue, Field} from "../types/api";
import {AuthContext, ROUTES} from "../App";
import {Navigate} from "react-router-dom";

export enum AuthFormMode
{
    login,
    registration,
}

export interface AuthFormProps
{
    mode: AuthFormMode
}

interface FormConfig
{
    submitLabel: string;
    fields: Field[];
    submitHandler: (inputs: DataValue[]) => Promise<void>;
    alertMessage: string;
}

const AuthForm: FC<AuthFormProps> = ({mode}) =>
{
    const { user, setUser, checkAuth } = useContext(AuthContext);

    const [redirectTo, setRedirectTo] = useState<string | null>(null);
    const [menuMode, setMenuMode] = useState<AuthFormMode>(mode);
    const [formConfig, setFormConfig] = useState<Record<AuthFormMode, FormConfig>>({
        [AuthFormMode.login]: {
            submitLabel: "",
            fields: [],
            submitHandler: async () => {},
            alertMessage: ""
        },
        [AuthFormMode.registration]: {
            submitLabel: "",
            fields: [],
            submitHandler: async () => {},
            alertMessage: ""
        }
    });
    const [loading, setLoading] = useState<boolean>(true);

    useEffect(() =>
    {
        requestAndLoadFields();
    }, []);

    const updateFormConfig = (mode: AuthFormMode, newConfig: Partial<FormConfig>) => {
        setFormConfig(prev => {
            if (!prev) return { [mode]: newConfig } as Record<AuthFormMode, FormConfig>;
            return {
                ...prev,
                [mode]: {
                    ...prev[mode],
                    ...newConfig
                }
            };
        });
    };

    const requestAndLoadFields = async () =>
    {
        try
        {
            const loginFieldsPromise = getLoginFields();
            const registerCompanyFieldsPromise = getCompanyRegistrationFields();

            const loginFields = await loginFieldsPromise;
            const registerCompanyFields = await registerCompanyFieldsPromise;

            const config: Record<AuthFormMode, FormConfig> = {
                [AuthFormMode.login]: {
                    submitLabel: "Войти",
                    fields: loginFields,
                    submitHandler: requestLogin,
                    alertMessage: ""},
                [AuthFormMode.registration]: {
                    submitLabel: "Зарегистрировать компанию",
                    fields: registerCompanyFields,
                    submitHandler: sendCompanyCreateRequest,
                    alertMessage: ""}}

            setFormConfig(config)
        }
        catch (error)
        {
            console.log('Failed to load form fields:', error);
            updateFormConfig(menuMode, {alertMessage: "Не удалось загрузить форму"})
        }
        finally
        {
            setLoading(false);
        }
    };

    const sendCompanyCreateRequest = async (dataValues: DataValue[]) =>
    {
        try
        {
            updateFormConfig(menuMode, {alertMessage: ""})
            const user = await createCompany(dataValues);
            if (user)
            {
                await checkAuth()
                if (user) setRedirectTo(ROUTES.MAIN);
            }
        }
        catch (error)
        {
            if (error instanceof Error) updateFormConfig(menuMode, {alertMessage: error.message})
        }
    }

    const requestLogin = async (dataValues: DataValue[]) =>
    {
        try
        {
            updateFormConfig(menuMode, {alertMessage: ""})
            const user = await login(dataValues);
            if (user)
            {
                await checkAuth()
                if (user) setRedirectTo(ROUTES.MAIN);
            }
        }
        catch (error)
        {
            if (error instanceof Error) {
                updateFormConfig(menuMode, {alertMessage: error.message})
            }
        }
    }

    const getForm = (): ReactElement =>
    {
        if (!formConfig) return <div>Загрузка формы</div>

        const config = formConfig[menuMode];

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

                <Form key={menuMode}
                    submitLabel={config.submitLabel}
                    inputs={config.fields.map((field) => {
                        return {inputData: field}
                    })}
                    onSubmit={config.submitHandler}/>
                <p>{config.alertMessage}</p>

                <Button onClick={async () => console.log("аутентифицирован: " + user?.username + " " + user?.isCompanySuperuser)} variant={ButtonType.general} text={"Аутентифицирован?"}/><br/>
            </div>)
    }

    if (redirectTo) {
        return <Navigate to={redirectTo} replace/>;
    }
    return loading ? <div>Загрузка</div> : getForm();
}

export default AuthForm;