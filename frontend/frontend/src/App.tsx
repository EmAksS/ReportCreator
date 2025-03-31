import React from "react";
import "./App.css";
import Hat from "./components/Hat";
import {ButtonType} from "./components/Button";
import AuthForm, {AuthFormMode} from "./components/AuthForm";


function App() {
  return (
      <div className={"page"}>
        <Hat imageSrc={"/assets/images/report_creator_logo.png"} title={"Report Creator"}
             buttonProps={[
                 {text: "Личный кабинет", onClick: ()=>{}, variant: ButtonType.hat},
                 {text: "Выйти", onClick: ()=>{}, variant: ButtonType.hat}]}/>

        <AuthForm mode={AuthFormMode.registration}/>

        <div className={"main-space"}>

        </div>
      </div>
  );
}

export default App;
