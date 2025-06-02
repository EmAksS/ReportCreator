import React, { FC, useState } from "react";
import TemplateCreationForm from "../TemplateCreationForm";
import SimpleContainer from "../SimpleContainer";
import DocumentCreationForm from "../DocumentCreationForm";
import Button, { ButtonType } from "../Button";
import DocumentShowMenu from "../forms/DocumentShowMenu";

const options = [
    { id: "create-document", text: "Создать документ" },
    { id: "create-template", text: "Создать шаблон" },
    { id: "show-documents", text: "Просмотр документов"}
];

const MainPage: FC = () => {
    const [selected, setSelected] = useState<string>("create-document");

    const renderContent = () => {
        switch (selected) {
            case "create-template":
                return <TemplateCreationForm />;
            case "create-document":
                return <DocumentCreationForm />;
            case "show-documents":
                return <DocumentShowMenu />;
            default:
                return null;
        }
    };

    return (
        <div style={{ display: "flex"}}>
            <SimpleContainer style={{width: "500px", height: "fit-content", display: "inline-block"}}>
                {options.map((opt) => (
                    <div>
                        <Button
                        key={opt.id}
                        text={opt.text}
                        variant={ButtonType.toggleable}
                        style={{width: "100%"}}
                        selected={opt.id === selected}
                        onClick={() => setSelected(opt.id)}/>
                        <br/>
                    </div>
                ))}
            </SimpleContainer>

            <SimpleContainer
                style={{ width: 600, display: "inline-block", height: "fit-content" }}>
                {renderContent()}
            </SimpleContainer>
        </div>
    );
};

export default MainPage;
