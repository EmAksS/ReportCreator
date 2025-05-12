import React from "react";
import "./App.css";
import Hat from "./components/Hat";
import {ButtonType} from "./components/Button";
import {AuthFormMode} from "./components/AuthForm";
import {BrowserRouter, Route, Routes, useLocation} from "react-router-dom";
import AuthPage from "./components/pages/AuthPage";
import WelcomePage from "./components/pages/WelcomePage";

function AppContent()
{
    const location = useLocation();
    const shouldShowHatButtons = location.pathname === "/welcome";

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
                    <Route path="/register" element={<AuthPage authMode={AuthFormMode.registration}/>} />
                    <Route path="/login" element={<AuthPage authMode={AuthFormMode.login}/>} />
                    <Route path="/welcome" element={<WelcomePage/>} />
                </Routes>
            </div>
        </div>);
}

function App()
{
    return (
        <BrowserRouter>
            <AppContent/>
        </BrowserRouter>);
}

export default App;