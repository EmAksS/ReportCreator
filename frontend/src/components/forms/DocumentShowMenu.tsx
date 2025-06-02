import { FC, useEffect, useState } from "react";
import { DocumentData, DocumentTemplate } from "../../types/core";
import { downloadDocument, getDocuments, getTemplateInfo } from "../../api/api";
import Button, { ButtonType } from "../Button";

const DocumentShowMenu: FC = () => {
    const [documents, setDocuments] = useState<DocumentData[]>([]);
    const [templatesInfo, setTemplatesInfo] = useState<DocumentTemplate[]>([]);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchDocs = async () => {
            setLoading(true);
            setError(null);
            try {
                const docs = await getDocuments();
                setDocuments(docs);

                const infos = await Promise.all(docs.map((doc) => getTemplateInfo(doc.id)));
                setTemplatesInfo(infos);
            } catch (err: any) {
                setError(err.message || "Ошибка при загрузке документов");
            } finally {
                setLoading(false);
            }
        };

        fetchDocs();
    }, []);

    if (loading) {
        return <div>Загрузка документов…</div>;
    }

    if (error) {
        return <div className="error">Ошибка: {error}</div>;
    }

    if (!documents.length) {
        return <div>Нет существующих документов.</div>;
    }

    return (
        <div>
            <p>Существующие документы:</p>
            <ul style={{ listStyleType: "none", padding: 0 }}>
                {documents.map((doc, idx) => {
                    const tpl = templatesInfo[idx];
                    const title = tpl
                        ? `${tpl.templateType} "${tpl.templateName}" #${doc.id}`
                        : `Document #${doc.id}`;

                    return (
                        <li key={doc.id} style={{ display: "flex", alignItems: "center", gap: "1rem", marginBottom: "0.5rem" }}>
                            <span>{title}</span>
                            <Button text="Скачать" variant={ButtonType.general} onClick={() => downloadDocument(doc.id)} />
                        </li>
                    );
                })}
            </ul>
        </div>);
};

export default DocumentShowMenu;
