import React, {createContext, ReactNode, useContext, useEffect, useState} from "react";
import "./App.css";
import Hat from "./components/Hat";
import { ButtonType } from "./components/Button";
import { AuthFormMode } from "./components/forms/AuthForm";
import {BrowserRouter, Navigate, Route, Routes, useLocation, useNavigate} from "react-router-dom";
import AuthPage from "./components/pages/AuthPage";
import { getUser, logout } from "./api/api";
import MainPage from "./components/pages/MainPage";
import CompanyPage from "./components/pages/CompanyPage";
import ModalContextProvider from "./components/contexts/ModalContextProvider";
import AuthContextProvider, {AuthContext} from "./components/contexts/AuthContextProvider";

export const ROUTES = {
    LOGIN: "/login",
    REGISTRATION: "/register",
    WELCOME: "/welcome",
    MAIN: "/main",
    COMPANY: "/company",
    DOCUMENTS: "/documents",
}

function AppContent()
{
    const { user, checkAuth, isAuthChecked } = useContext(AuthContext);
    const location = useLocation();
    const navigate = useNavigate();

    useEffect(() => {
        if (!isAuthChecked) return;

        if (!user && ![ROUTES.LOGIN, ROUTES.REGISTRATION].includes(location.pathname)) {
            navigate(ROUTES.LOGIN);
        } else if (user && [ROUTES.LOGIN, ROUTES.REGISTRATION].includes(location.pathname)) {
            navigate(ROUTES.MAIN);
        }
    }, [location.pathname, user, isAuthChecked]);

    if (!user && !isAuthChecked) return null;

    return (
        <div className={"page"}>
            <Hat
                imageSrc={"/assets/images/logo.png"}
                title={"Report Creator"}
                onLogoClick={() => {if (user) navigate(ROUTES.MAIN)}}
                buttonProps={user
                    ? [{ text: "Главная", onClick: () => navigate(ROUTES.MAIN), variant: ButtonType.hat },
                        { text: "Компания", onClick: () => navigate(ROUTES.COMPANY), variant: ButtonType.hat },
                        { text: "Выйти", onClick: async () => { await logout(); await checkAuth(); navigate(ROUTES.MAIN); }, variant: ButtonType.hat }]
                    : []}/>

            <div className={"main-space"}>
                <Routes>
                    <Route path={ROUTES.REGISTRATION} element={<AuthPage authMode={AuthFormMode.registration} />} />
                    <Route path={ROUTES.LOGIN} element={<AuthPage authMode={AuthFormMode.login} />} />
                    <Route path={ROUTES.MAIN} element={<MainPage />} />
                    <Route path={ROUTES.COMPANY} element={<CompanyPage />} />
                    <Route path="*" element={<Navigate to={ROUTES.MAIN} />} />
                </Routes>
            </div>
        </div>
    );
}

function App()
{
    return (
        <BrowserRouter>
            <AuthContextProvider>
                <ModalContextProvider>
                    <AppContent/>
                </ModalContextProvider>
            </AuthContextProvider>
        </BrowserRouter>);
}


export default App;