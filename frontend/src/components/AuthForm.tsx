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
import {useNavigate} from "react-router-dom";
import {User} from "../types/core";
import SimpleContainer from "./SimpleContainer";

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

const AuthForm: FC<AuthFormProps> = (props: AuthFormProps) =>
{
    const { user, checkAuth } = useContext(AuthContext);
    const navigate = useNavigate();

    const [menuMode, setMenuMode] = useState<AuthFormMode>(props.mode);
    const [isLoading, setIsLoading] = useState(true);
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

    useEffect(() =>
    {
        requestFields();
    }, [props.mode]);

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

    const requestFields = async () =>
    {
        try
        {
            const [loginFields, registerCompanyFields] = await Promise.all(
                [getLoginFields(), getCompanyRegistrationFields()]);

            const config: Record<AuthFormMode, FormConfig> = {
                [AuthFormMode.login]: {
                    submitLabel: "Войти",
                    fields: loginFields,
                    submitHandler: requestLogin,
                    alertMessage: ""},
                [AuthFormMode.registration]: {
                    submitLabel: "Зарегистрировать компанию",
                    fields: registerCompanyFields,
                    submitHandler: requestCreateCompany,
                    alertMessage: ""}}

            setFormConfig(config)
            setIsLoading(false)
        }
        catch (error)
        {
            if (error instanceof Error)
            {
                updateFormConfig(menuMode, {alertMessage: error.message});
            }
            console.log("Не удалось загрузить поля", error);
        }
    };

    const requestCreateCompany = async (dataValues: DataValue[]) =>
    {
        await authRequest(dataValues, createCompany)
    }

    const requestLogin = async (dataValues: DataValue[]) =>
    {
        await authRequest(dataValues, login)
    }

    const authRequest = async (
        dataValues: DataValue[],
        requestFunction: (data: DataValue[]) => Promise<User>): Promise<void> =>
    {
        try
        {
            updateFormConfig(menuMode, {alertMessage: ""})
            if (await requestFunction(dataValues))
            {
                if (await checkAuth()) navigate(ROUTES.MAIN);
            }
        }
        catch (error)
        {
            if (error instanceof Error)
            {
                updateFormConfig(menuMode, {alertMessage: error.message});
            }
            console.log("Не удалось аутентифицироваться", error);
        }
    }

    const getForm = (): ReactElement =>
    {
        if (isLoading) return <div>Загрузка формы</div>

        const config = formConfig[menuMode];

        return (
            <SimpleContainer style={{}} className={"authorization-form"}>
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
                <p className={"alert-message"}>{config.alertMessage}</p>
            </SimpleContainer>)
    }

    return getForm();
}

export default AuthForm;