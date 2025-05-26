import React, {FC} from "react";
import TemplateCreationForm from "../TemplateCreationForm";
import SimpleContainer from "../SimpleContainer";

const MainPage: FC = () =>
{
    return (
        <SimpleContainer style={{width: "500px"}}>
            <TemplateCreationForm />
        </SimpleContainer>)
}

export default MainPage;
