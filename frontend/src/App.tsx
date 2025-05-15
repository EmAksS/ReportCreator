import React, { createContext, useContext, useEffect, useState } from "react";
import "./App.css";
import Hat from "./components/Hat";
import { ButtonType } from "./components/Button";
import { AuthFormMode } from "./components/AuthForm";
import { BrowserRouter, Navigate, Route, Routes, useLocation } from "react-router-dom";
import AuthPage from "./components/pages/AuthPage";
import WelcomePage from "./components/pages/WelcomePage";
import { isAuthenticated, requestLogout } from "./api/api";

export const ROUTES = {
    LOGIN: "/login",
    REGISTRATION: "/register",
    WELCOME: "/welcome"
}

export interface AuthContextType {
    authState: boolean | null; // null - проверка ещё не завершена
    setAuthState: (value: boolean) => void;
    checkAuth: () => Promise<void>;
}

export const AuthContext = createContext<AuthContextType>({
    authState: null,
    setAuthState: () => {},
    checkAuth: async () => {}
});

function AppContent() {
    const { authState } = useContext(AuthContext);
    const location = useLocation();

    if (authState === null) { return <div>Загрузка...</div>; }

    if (!authState && location.pathname !== ROUTES.LOGIN) {
        return <Navigate to={ROUTES.LOGIN} replace />;
    }

    return (
        <div className={"page"}>
            <Hat
                imageSrc={"/assets/images/report_creator_logo.png"}
                title={"Report Creator"}
                buttonProps={authState
                    ? [{ text: "Личный кабинет", onClick: () => {}, variant: ButtonType.hat },
                        {text: "Выйти", onClick: async () => {await requestLogout(); window.location.reload(); }, variant: ButtonType.hat}]
                    : []}/>

            <div className={"main-space"}>
                <Routes>
                    <Route path={ROUTES.REGISTRATION} element={<AuthPage authMode={AuthFormMode.registration} />} />
                    <Route path={ROUTES.LOGIN} element={<AuthPage authMode={AuthFormMode.login} />} />
                    <Route path={ROUTES.WELCOME} element={<WelcomePage />} />
                </Routes>
            </div>
        </div>
    );
}

function App() {
    const [authState, setAuthState] = useState<boolean | null>(null);

    const checkAuth = async () => {
        try {
            const isAuth = await isAuthenticated();
            setAuthState(isAuth);
        } catch (error) {
            console.error("Auth check failed:", error);
            setAuthState(false);
        }
    };

    useEffect(() => {
        checkAuth();
    }, []);

    return (
        <BrowserRouter>
            <AuthContext.Provider value={{ authState, setAuthState, checkAuth}}>
                <AppContent/>
            </AuthContext.Provider>
        </BrowserRouter>
    );
}

export default App;