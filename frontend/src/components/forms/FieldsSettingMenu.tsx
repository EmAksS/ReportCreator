import React, {FC, useEffect, useState} from "react";
import {DataValue, Field} from "../../types/api";
import {createTemplateField, getTemplateFieldsFields} from "../../api/api";
import {DocumentTemplate} from "../../types/core";
import Form from "../Form";
import {InputProps} from "../Input";

export interface FieldsSettingMenuProps {
    template: DocumentTemplate;
}

const FieldsSettingMenu: FC<FieldsSettingMenuProps> = ({template}) => {
    const [currentFieldId, setCurrentFieldId] = useState<number>(0);
    const [fieldNames, setFieldNames] = useState<string[]>([]);
    const [fields, setFields] = useState<Field[][]>([]);
    const [isLoading, setIsLoading] = useState<boolean>(false);

    useEffect(() => {
        setFieldNames(template.foundFields);
        requestFields();
    }, [template]);

    const requestFields = async () => {
        setIsLoading(true);
        try {
            const fieldsRequests = template.foundFields.map(_ =>
                getTemplateFieldsFields(template.id)
            );
            const requestedFields = await Promise.all(fieldsRequests);
            setFields(requestedFields);
        } catch (error) {
            console.error("Error fetching fields:", error);
        } finally {
            setIsLoading(false);
        }
    };

    const onFieldSettingSubmit = async (values: DataValue[]) => {
        // 1) Перезапишем value для ключа 'keyName', если он есть
        // 2) Если нет — добавим его
        const enhancedValues = values
            .map(v =>
                v.fieldId === "key_name"
                    ? { ...v, value: fieldNames[currentFieldId] }
                    : v
            )
            .concat(
                values.some(v => v.fieldId === "key_name")
                    ? []
                    : { fieldId: "key_name", value: fieldNames[currentFieldId] }
            );

        try {
            await createTemplateField(template.id, enhancedValues);
            removeFieldById(currentFieldId);
        } catch (error) {
            console.error("Error creating template field:", error);
        }
    };

    const removeFieldById = (id: number) => {
        setFieldNames(prev =>
            prev.filter((_, idx) => idx !== id)
        );
        setFields(prev => prev.filter((_, idx) => idx !== id));
        setCurrentFieldId(id === 0 ? 0 : id - 1);
    };

    const handlePrevField = () =>
        setCurrentFieldId(i => Math.max(0, i - 1));
    const handleNextField = () =>
        setCurrentFieldId(i => Math.min(fieldNames.length - 1, i + 1));

    if (isLoading) return <div>Loading...</div>;

    // Берём только те поля, у которых fieldId !== 'keyName'
    const visibleFields =
        fields[currentFieldId]?.filter(f => f.keyName !== "key_name") || [];

    return (
        <div>
            <h3>Настройка полей для шаблона {template.templateName}</h3>

            {fieldNames.length > 0 && (
                <div
                    style={{
                        display: "flex",
                        justifyContent: "space-between",
                        margin: "20px 0",
                    }}
                >
                    <button
                        onClick={handlePrevField}
                        disabled={currentFieldId === 0}
                    >
                        ← Предыдущее поле
                    </button>

                    <div>
                        Поле {fieldNames[currentFieldId]} ({currentFieldId + 1} из {fieldNames.length})
                    </div>

                    <button
                        onClick={handleNextField}
                        disabled={
                            currentFieldId === fieldNames.length - 1 ||
                            fieldNames.length === 0
                        }
                    >
                        Следующее поле →
                    </button>
                </div>
            )}

            {visibleFields.length > 0 ? (
                <Form
                    key={fieldNames[currentFieldId]}
                    inputs={visibleFields.map(
                        field => ({ inputData: field } as InputProps)
                    )}
                    onSubmit={onFieldSettingSubmit}
                    submitLabel="Сохранить данные поля"
                />
            ) : (
                <div>
                    {fieldNames.length === 0
                        ? "Все поля сохранены"
                        : "Нет доступных полей для настройки"}
                </div>
            )}
        </div>
    );
};

export default FieldsSettingMenu;
