import { FC, JSX } from "react";

export interface ListItem {
    id: number;
    content: JSX.Element;
}

export interface ListProps {
    items: ListItem[];
    onAdd?: () => void;
    onRemove?: (id: number) => void;
    hideAddButton?: boolean;   // Скрывает кнопку "+"
    hideRemoveButtons?: boolean; // Скрывает кнопки "-"
}

const List: FC<ListProps> = ({ items, onAdd, onRemove, hideAddButton = false, hideRemoveButtons = false }) => {
    return (
        <div className="list">
            {items.map(item => (
                <div key={item.id} className="list-item">
                    {item.content}
                    {!hideRemoveButtons && (
                        <button className="list-item-remove-button" onClick={() => onRemove?.(item.id)}>
                            -
                        </button>
                    )}
                </div>
            ))}
            {!hideAddButton && (
                <button className="list-item-add-button" onClick={onAdd}>
                    +
                </button>
            )}
        </div>
    );
};

export default List;
