import React, {FC} from "react";
import SimpleContainer from "../SimpleContainer";
import DocumentCreationForm from "../DocumentCreationForm";

const DocumentPage: FC = () =>
{
    return (
        <SimpleContainer style={{width: "500px"}}>
            <DocumentCreationForm />
        </SimpleContainer>)
}

export default DocumentPage;
