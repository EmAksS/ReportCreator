import {FC, ReactElement, useEffect, useState} from "react";
import Form from "./Form";
import Button, {ButtonType} from "./Button";
import {
    getLoginFields,
    getRegisterCompanyFields,
    isAuthenticated,
    requestCreateCompany,
    requestLogin
} from "../api/api";
import {DataValue, Field, InputPresentation} from "../types/api";

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
    fields: Field[];
    submitHandler: (inputs: InputPresentation[]) => Promise<void>;
    alertMessage: string;
}

const AuthForm: FC<AuthFormProps> = ({mode}) =>
{
    const [menuMode, setMenuMode] = useState<AuthFormMode>(mode);
    const [formConfig, setFormConfig] = useState<Record<AuthFormMode, FormConfig>>({
        [AuthFormMode.login]: {
            fields: [],
            submitHandler: async () => {},
            alertMessage: ""
        },
        [AuthFormMode.registration]: {
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
            const registerCompanyFieldsPromise = getRegisterCompanyFields();

            const loginFields = await loginFieldsPromise;
            const registerCompanyFields = await registerCompanyFieldsPromise;

            const config: Record<AuthFormMode, FormConfig> = {
                [AuthFormMode.login]: {
                    fields: loginFields,
                    submitHandler: sendLoginRequest,
                    alertMessage: ""},
                [AuthFormMode.registration]: {
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

    const sendCompanyCreateRequest = async (inputs: InputPresentation[]) =>
    {
        try
        {
            if (requiredFieldsNotEmpty(inputs))
            {
                const dataValues: DataValue[] = getDataValues(inputs);
                updateFormConfig(menuMode, {alertMessage: ""})
                requestCreateCompany(dataValues);
            }
        }
        catch (error)
        {
            if (error instanceof Error) updateFormConfig(menuMode, {alertMessage: error.message})
        }
    }

    const sendLoginRequest = async (inputs: InputPresentation[]) =>
    {
        try
        {
            if (requiredFieldsNotEmpty(inputs))
            {
                const dataValues: DataValue[] = getDataValues(inputs);
                updateFormConfig(menuMode, {alertMessage: ""})
                await requestLogin(dataValues);
            }
        }
        catch (error)
        {
            if (error instanceof Error) {
                console.log("поймана ошибка: " + error.message)
                updateFormConfig(menuMode, {alertMessage: error.message})
            }
        }
    }

    const requiredFieldsNotEmpty = (inputs: InputPresentation[]): boolean =>
    {
        for (let i = 0; i < inputs.length; i++)
        {
            const field = inputs[i];
            if ((field.value.value === undefined || field.value.value === "") && inputs[i].field.isRequired)
            {
                updateFormConfig(menuMode, {alertMessage: "Заполните поле " + field.field.name})
                return false;
            }
        }
        return true;
    }

    const getDataValues = (fields: InputPresentation[]): DataValue[] =>
    {
        const dataValues: DataValue[] = [];

        for (let i = 0; i < fields.length; i++)
        {
            const input = fields[i];
            const field = input.field
            const value = input.value

            if (!value.value)
            {
                if (!field.isRequired) input.value.value = "";
                else throw Error(`Поле "${field.name}" должно быть заполнено`)
            }
            dataValues.push({fieldId: value.fieldId, value: value.value} as DataValue)
        }

        return dataValues
    }

    const getForm = (): ReactElement =>
    {
        if (!formConfig) return <div>Загрузка формы</div>

        const config = formConfig[menuMode];

        return <Form
            inputs={config.fields.map((field) => {
                return {inputData: field}
            })}
            onSubmit={config.submitHandler}
            alertMessage={config.alertMessage}/>;
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
            <Button onClick={async () => console.log("аутентифицирован: " + await isAuthenticated())} variant={ButtonType.general} text={"Аутентифицирован?"}/>
        </div>
    )
}

export default AuthForm;