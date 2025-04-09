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
                    style={{width: "300px"}}
                    inputs={[
                        {inputData: {name: "text1", keyName: "name1", placeholder: "popa1", validationRegEx: new RegExp(/^[A-Za-zА-Яа-яЁё]+$/), isRequired: true, inputType: "text"}},
                        {inputData: {name: "text2", keyName: "name2", placeholder: "popa2", validationRegEx: new RegExp(/^[A-Za-zА-Яа-яЁё]+$/), isRequired: true, inputType: "text"}}]}
                    onSubmit={(data) =>
                    {
                        console.log(data)
                    }}
                    buttons={[{
                        type: "submit",
                        text: "Войти",
                        onClick: ()=>{},
                        style: {width: "100%", marginTop: "18px"},
                        variant: ButtonType.general}]}/>;

            case AuthFormMode.registration:
                return <Form
                    inputs={[
                        {inputData: {name: "text1", keyName: "name1", placeholder: "popa1", isRequired: true, inputType: "text", secureText: true}},
                        {inputData: {name: "text2", keyName: "name2", placeholder: "popa2", isRequired: true, inputType: "text", secureText: true}}]}
                    onSubmit={(data) =>
                    {
                        data.forEach((inputData) =>
                        {
                            console.log(inputData)
                        })
                    }}
                    buttons={[{
                        type: "submit",
                        text: "Войти",
                        onClick: ()=>{},
                        style: {width: "100%", marginTop: "18px"},
                        variant: ButtonType.general}]}/>;
        }
    }

    return (
        <div className={"authorization-form"}>
            {getForm()}
        </div>
    )
}

export default AuthForm;