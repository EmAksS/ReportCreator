import React, { createContext, useContext, useEffect, useState } from "react";
import "./App.css";
import Hat from "./components/Hat";
import { ButtonType } from "./components/Button";
import { AuthFormMode } from "./components/AuthForm";
import {BrowserRouter, Navigate, Route, Routes, useLocation, useNavigate} from "react-router-dom";
import AuthPage from "./components/pages/AuthPage";
import WelcomePage from "./components/pages/WelcomePage";
import { getUser, logout } from "./api/api";
import MainPage from "./components/pages/MainPage";
import CompanyPage from "./components/pages/CompanyPage";
import {User} from "./types/core";

export const ROUTES = {
    LOGIN: "/login",
    REGISTRATION: "/register",
    WELCOME: "/welcome",
    MAIN: "/main",
    COMPANY: "/company"
}

export interface UserContextType {
    user: User | null;
    setUser: (value: User) => void;
    checkAuth: () => Promise<void>;
}

export const AuthContext = createContext<UserContextType>({
    user: null,
    setUser: () => {},
    checkAuth: async () => {}
});

function AppContent() {
    const { user } = useContext(AuthContext);
    const location = useLocation();
    const navigate = useNavigate();

    if (!user && location.pathname !== ROUTES.LOGIN && location.pathname !== ROUTES.REGISTRATION) {
        return <Navigate to={ROUTES.LOGIN} replace />;
    }

    return (
        <div className={"page"}>
            <Hat
                imageSrc={"/assets/images/report_creator_logo.png"}
                title={"Report Creator"}
                buttonProps={user
                    ? [{ text: "Компания", onClick: () => navigate(ROUTES.COMPANY), variant: ButtonType.hat },
                        { text: "Личный кабинет", onClick: () => navigate(ROUTES.MAIN), variant: ButtonType.hat }, // Перенаправление на /main
                        { text: "Выйти", onClick: async () => { await logout(); window.location.reload(); }, variant: ButtonType.hat }]
                    : []}/>

            <div className={"main-space"}>
                <Routes>
                    <Route path={ROUTES.REGISTRATION} element={<AuthPage authMode={AuthFormMode.registration} />} />
                    <Route path={ROUTES.LOGIN} element={<AuthPage authMode={AuthFormMode.login} />} />
                    <Route path={ROUTES.WELCOME} element={<WelcomePage />} />
                    <Route path={ROUTES.MAIN} element={<MainPage />} />
                    <Route path={ROUTES.COMPANY} element={<CompanyPage />} />
                </Routes>
            </div>
        </div>
    );
}

function App() {
    const [authState, setAuthState] = useState<User | null>(null);

    const checkAuth = async () => {
        try {
            const isAuth = await getUser();
            setAuthState(isAuth);
        } catch (error) {
            console.error("Auth check failed:", error);
            setAuthState(null);
        }
    };

    useEffect(() => {
        checkAuth();
    }, []);

    return (
        <BrowserRouter>
            <AuthContext.Provider value={{ user: authState, setUser: setAuthState, checkAuth}}>
                <AppContent/>
            </AuthContext.Provider>
        </BrowserRouter>
    );
}

export default App;