import {FC, ReactElement, useState} from "react";
import Form from "./Form";
import {ButtonType} from "./Button";

export interface AuthFormProps
{
    mode: AuthFormMode
}

export enum AuthFormMode
{
    login,
    registration,
}

const AuthForm: FC<AuthFormProps> = ({mode}) =>
{
    const [menuMode, setMenuMode] = useState<AuthFormMode>(mode);

    const getForm = (): ReactElement =>
    {
        switch (menuMode)
        {
            case AuthFormMode.login:
                return <Form
                    textInputInfo={[
                        ["Логин"],
                        ["Пароль", {secureText: true}]]}
                    buttonInfo={[{
                        text: "Войти",
                        onClick: ()=>{},
                        style: {width: "100%", marginTop: "18px"},
                        variant: ButtonType.general}]}/>;

            case AuthFormMode.registration:
                return <Form
                    textInputInfo={[
                        ["Полное название компании"],
                        ["ФИО директора"],
                        ["Логин"],
                        ["Пароль", {secureText: true}]]}
                    buttonInfo={[{
                        text: "Зарегистрироваться",
                        onClick: ()=>{},
                        style: {width: "100%", marginTop: "18px"},
                        variant: ButtonType.general},]}/>;
        }
    }

    return (
        <div className={"authorization-form"}>
            {getForm()}
        </div>
    )
}

export default AuthForm;