import React, { FC, useEffect, useState } from "react";
import { DataValue, Field } from "../../types/api";
import {
    createTemplateField,
    createTemplateTableField,
    getTemplateFieldsFields,
    getTemplateTableFieldSettingFields,
    getTemplateTableFieldValues,
} from "../../api/api";
import { DocumentTemplate } from "../../types/core";
import Form from "../Form";
import { InputProps } from "../Input";

export interface FieldsSettingMenuProps {
    template: DocumentTemplate;
}

const FieldsSettingMenu: FC<FieldsSettingMenuProps> = ({ template }) => {
    const [currentPhase, setCurrentPhase] = useState<"ordinary" | "table">("ordinary");

    const [ordinaryFieldNames, setOrdinaryFieldNames] = useState<string[]>([]);
    const [ordinaryFieldFields, setOrdinaryFieldFields] = useState<Field[][]>([]);
    const [currentOrdinaryIndex, setCurrentOrdinaryIndex] = useState<number>(0);

    const [tableFieldKeyNames, setTableFieldKeyNames] = useState<string[]>([]);
    const [tableFieldDisplayNames, setTableFieldDisplayNames] = useState<string[]>([]);
    const [tableFieldFields, setTableFieldFields] = useState<Field[][]>([]);
    const [currentTableIndex, setCurrentTableIndex] = useState<number>(0);

    const [isLoading, setIsLoading] = useState<boolean>(false);

    useEffect(() => {
        setCurrentPhase("ordinary");
        setCurrentOrdinaryIndex(0);
        setCurrentTableIndex(0);
        setOrdinaryFieldNames([]);
        setOrdinaryFieldFields([]);
        setTableFieldKeyNames([]);
        setTableFieldDisplayNames([]);
        setTableFieldFields([]);

        const fetchAllFields = async () => {
            setIsLoading(true);
            try {
                const ordNames = [...template.foundFields];
                setOrdinaryFieldNames(ordNames);

                const ordinaryRequests = ordNames.map(() => getTemplateFieldsFields(template.id));
                const ordFieldsArray = await Promise.all(ordinaryRequests);
                setOrdinaryFieldFields(ordFieldsArray);

                const tableNameFields = await getTemplateTableFieldValues(template.id);
                const tblKeyNames = tableNameFields.map((f) => f.keyName);
                const tblDisplayNames = tableNameFields.map((f) => f.name);
                setTableFieldKeyNames(tblKeyNames);
                setTableFieldDisplayNames(tblDisplayNames);

                const tableRequests = tblKeyNames.map(() => getTemplateTableFieldSettingFields(template.id));
                const tblFieldsArray = await Promise.all(tableRequests);
                setTableFieldFields(tblFieldsArray);
            } catch (error) {
                console.error("Error fetching fields:", error);
            } finally {
                setIsLoading(false);
            }
        };

        fetchAllFields();
    }, [template]);

    const onFieldSettingSubmit = async (values: DataValue[]) => {
        const isOrdinaryPhase = currentPhase === "ordinary";

        const keyNamesArr = isOrdinaryPhase ? ordinaryFieldNames : tableFieldKeyNames;
        const idx = isOrdinaryPhase ? currentOrdinaryIndex : currentTableIndex;

        const currentKeyName = keyNamesArr[idx];

        const hasKeyName = values.some((v) => v.fieldId === "key_name");
        const enhancedValues = values
            .map((v) => (v.fieldId === "key_name" ? { ...v, value: currentKeyName } : v))
            .concat(hasKeyName ? [] : { fieldId: "key_name", value: currentKeyName });

        try {
            if (isOrdinaryPhase) {
                await createTemplateField(template.id, enhancedValues);
                removeOrdinaryFieldByIndex(idx);
            } else {
                await createTemplateTableField(template.id, enhancedValues);
                removeTableFieldByIndex(idx);
            }
        } catch (error) {
            console.error("Error saving field settings:", error);
        }
    };

    const removeOrdinaryFieldByIndex = (index: number) => {
        setOrdinaryFieldNames((prev) => prev.filter((_, idx) => idx !== index));
        setOrdinaryFieldFields((prev) => prev.filter((_, idx) => idx !== index));
        setCurrentOrdinaryIndex((prevIdx) => {
            if (index === 0) return 0;
            return prevIdx > 0 ? prevIdx - 1 : 0;
        });
    };

    const removeTableFieldByIndex = (index: number) => {
        setTableFieldKeyNames((prev) => prev.filter((_, idx) => idx !== index));
        setTableFieldDisplayNames((prev) => prev.filter((_, idx) => idx !== index));
        setTableFieldFields((prev) => prev.filter((_, idx) => idx !== index));
        setCurrentTableIndex((prevIdx) => {
            if (index === 0) return 0;
            return prevIdx > 0 ? prevIdx - 1 : 0;
        });
    };

    const handlePrev = () => {
        if (currentPhase === "ordinary") {
            setCurrentOrdinaryIndex((i) => Math.max(0, i - 1));
        } else {
            setCurrentTableIndex((i) => Math.max(0, i - 1));
        }
    };

    const handleNext = () => {
        if (currentPhase === "ordinary") {
            if (currentOrdinaryIndex < ordinaryFieldNames.length - 1) {
                setCurrentOrdinaryIndex((i) => i + 1);
            } else {
                if (tableFieldKeyNames.length > 0) {
                    setCurrentPhase("table");
                    setCurrentTableIndex(0);
                }
            }
        } else {
            if (currentTableIndex < tableFieldKeyNames.length - 1) {
                setCurrentTableIndex((i) => i + 1);
            }
        }
    };

    if (isLoading) {
        return <div>Loading...</div>;
    }

    if (
        currentPhase === "ordinary" &&
        ordinaryFieldNames.length === 0 &&
        tableFieldKeyNames.length > 0
    ) {
        setCurrentPhase("table");
        setCurrentTableIndex(0);
        return null;
    }

    if (currentPhase === "table" && tableFieldKeyNames.length === 0) {
        return <div>Все поля сохранены</div>;
    }

    if (ordinaryFieldNames.length === 0 && tableFieldKeyNames.length === 0) {
        return <div>Все поля сохранены</div>;
    }

    const isOrdinaryPhase = currentPhase === "ordinary";
    const displayNamesArr = isOrdinaryPhase ? ordinaryFieldNames : tableFieldDisplayNames;
    const activeFieldsArray = isOrdinaryPhase ? ordinaryFieldFields : tableFieldFields;
    const activeIndex = isOrdinaryPhase ? currentOrdinaryIndex : currentTableIndex;

    const currentLabel = isOrdinaryPhase
        ? `Поле ${displayNamesArr[activeIndex]} (${activeIndex + 1} из ${displayNamesArr.length})`
        : `Табличное поле ${displayNamesArr[activeIndex]} (${activeIndex + 1} из ${displayNamesArr.length})`;

    const visibleFields = activeFieldsArray[activeIndex]?.filter(
        (f) => f.keyName !== "key_name" && f.keyName !== "related_template"
    ) || [];

    return (
        <div style={{width:"700px"}}>
            <h3>Настройка полей для шаблона {template.templateName}</h3>
            {displayNamesArr.length > 0 && (
                <div
                    style={{
                        display: "flex",
                        justifyContent: "space-between",
                        margin: "20px 0",
                    }}
                >
                    <button className={"toggleable-button"} onClick={handlePrev} disabled={activeIndex === 0}>
                        ← Предыдущее
                    </button>

                    <div>{currentLabel}</div>

                    <button className={"toggleable-button"}
                            onClick={handleNext}
                        disabled={
                            isOrdinaryPhase
                                ? currentOrdinaryIndex === ordinaryFieldNames.length - 1 && tableFieldKeyNames.length === 0
                                : currentTableIndex === tableFieldKeyNames.length - 1
                        }
                    >
                        Следующее →
                    </button>
                </div>
            )}

            {visibleFields.length > 0 ? (
                <Form
                    key={displayNamesArr[activeIndex]}
                    inputs={visibleFields.map((field) => ({ inputData: field } as InputProps))}
                    onSubmit={onFieldSettingSubmit}
                    submitLabel="Сохранить данные поля"
                />
            ) : (
                <div>Нет доступных полей для настройки</div>
            )}
        </div>
    );
};

export default FieldsSettingMenu;
