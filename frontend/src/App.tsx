import React, {createContext, useContext, useEffect, useState} from "react";
import "./App.css";
import Hat from "./components/Hat";
import {ButtonType} from "./components/Button";
import {AuthFormMode} from "./components/AuthForm";
import {BrowserRouter, Navigate, Route, Routes, useLocation} from "react-router-dom";
import AuthPage from "./components/pages/AuthPage";
import WelcomePage from "./components/pages/WelcomePage";
import {isAuthenticated} from "./api/api";

const AuthContext = createContext<boolean>(false);

const ROUTES = {
    LOGIN: "/login",
    REGISTRATION: "/register",
    WELCOME: "/welcome"
}

function AppContent()
{
    const isAuthenticated = useContext(AuthContext);
    const location = useLocation();
    const shouldShowHatButtons = location.pathname === ROUTES.WELCOME;

    if (!isAuthenticated && location.pathname !== ROUTES.LOGIN) { return <Navigate to={ROUTES.LOGIN} replace/>; }

    return (
        <div className={"page"}>
            <Hat
                imageSrc={"/assets/images/report_creator_logo.png"}
                title={"Report Creator"}
                buttonProps={shouldShowHatButtons
                    ? [{text: "Личный кабинет", onClick: ()=>{}, variant: ButtonType.hat},
                       {text: "Выйти", onClick: ()=>{}, variant: ButtonType.hat}]
                    : []}
            />

            <div className={"main-space"}>
                <Routes>
                    <Route path={ROUTES.REGISTRATION} element={<AuthPage authMode={AuthFormMode.registration}/>} />
                    <Route path={ROUTES.LOGIN} element={<AuthPage authMode={AuthFormMode.login}/>} />
                    <Route path={ROUTES.WELCOME} element={<WelcomePage/>} />
                </Routes>
            </div>
        </div>);
}

function App()
{
    const [authState, setAuthState] = useState<boolean>(false);

    useEffect(() => {
        checkAuth();
    }, [])

    const checkAuth = async () =>
    {
        setAuthState(await isAuthenticated());
    };

    return (
        <BrowserRouter>
            <AuthContext.Provider value={authState}>
                <AppContent/>
            </AuthContext.Provider>
        </BrowserRouter>);
}

export default App;