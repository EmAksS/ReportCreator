import React, {FC} from "react";
import AuthForm, {AuthFormMode} from "../forms/AuthForm";


export interface AuthPageProps
{
    authMode: AuthFormMode;
}

const AuthPage: FC<AuthPageProps> = (props: AuthPageProps) =>
{
    return (
        <AuthForm mode={props.authMode}/>
    )
}

export default AuthPage;