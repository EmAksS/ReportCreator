import React, {createContext, ReactNode, useContext, useEffect, useState} from "react";
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
import Modal, {ModalProps} from "./components/Modal";

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
    checkAuth: () => Promise<boolean>;
}

export interface ModalContextType extends ModalProps
{
    setChildren: (value: ReactNode) => void;
    setIsOpen: (value: boolean) => void;
}

export const AuthContext = createContext<UserContextType>({
    user: null,
    setUser: () => {},
    checkAuth: async () => false
});

export const ModalContext = createContext<ModalContextType>({
    isOpen: false,
    setIsOpen: () => {},
    children: null,
    setChildren: () => {},
})

function AppContent()
{
    const { user, checkAuth } = useContext(AuthContext);
    const location = useLocation();
    const navigate = useNavigate();

    useEffect(() =>
    {
        if (!user && location.pathname !== ROUTES.LOGIN && location.pathname !== ROUTES.REGISTRATION)
        {
            navigate(ROUTES.LOGIN);
        }
    }, [user, location.pathname, navigate]);

    return (
        <div>
            <div className={"page"}>
                <Hat
                    imageSrc={"/assets/images/report_creator_logo.png"}
                    title={"Report Creator"}
                    buttonProps={user
                        ? [{ text: "Главная", onClick: () => navigate(ROUTES.MAIN), variant: ButtonType.hat },
                            { text: "Компания", onClick: () => navigate(ROUTES.COMPANY), variant: ButtonType.hat },
                            { text: "Выйти", onClick: async () => { await logout(); await checkAuth(); navigate(ROUTES.MAIN); }, variant: ButtonType.hat }]
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
        </div>

    );
}

function App()
{
    const [user, setUser] = useState<User | null>(null);
    const [isAuthChecked, setIsAuthChecked] = useState(false);

    const [isOpenModal, setIsOpenModal] = useState(false);
    const [modalChildren, setModalChildren] = useState<React.ReactNode>(null);

    const checkAuth = async (): Promise<boolean> =>
    {
        const user = await getUser();
        setUser(user);
        return user !== null;
    };

    useEffect(() =>
    {
        checkAuth().finally(() => setIsAuthChecked(true));
    }, []);

    return (
        <BrowserRouter>
            <AuthContext.Provider value={{ user, setUser, checkAuth }}>
                <ModalContext.Provider value={{
                    isOpen: isOpenModal,
                    setIsOpen: setIsOpenModal,
                    children: modalChildren,
                    setChildren: setModalChildren }}>
                    <Modal isOpen={isOpenModal} children={modalChildren} />
                    {isAuthChecked ? <AppContent/> : null}
                </ModalContext.Provider>
            </AuthContext.Provider>
        </BrowserRouter>
    );
}


export default App;