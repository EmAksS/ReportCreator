import React, {FC, ReactNode, useContext, useEffect} from "react";
import {ModalContext} from "./contexts/ModalContextProvider";

export interface ModalProps
{
    isOpen: boolean;
    children: ReactNode;
    onCancel?: () => void;
    onClose?: () => void;
    onOpen?: () => void;
}

const Modal: FC<ModalProps> = (props) =>
{
    const {isOpen, setIsOpen, onClose, onCancel, onOpen} = useContext(ModalContext);

    const onEscapePress = (event: KeyboardEvent) =>
    {
        if (event.key === "Escape") { setIsOpen(false); }
    };

    useEffect(() =>
    {
        if (isOpen) { document.addEventListener("keydown", onEscapePress); }
        return () => { document.removeEventListener("keydown", onEscapePress); };
    }, [isOpen]);

    return props.isOpen ?
        <div className={"modal"} onClick={() => setIsOpen(false)}>
            <div className={"modal-content"} onClick={(event) => event.stopPropagation()}>
                {props.children}
            </div>
        </div> : null
}

export default Modal;
