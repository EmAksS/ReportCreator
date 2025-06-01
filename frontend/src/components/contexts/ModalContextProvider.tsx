import React, {createContext, FC, ReactNode, useState} from "react";
import Modal, {ModalProps} from "../Modal";

export interface ModalContextType extends ModalProps
{
    setChildren: (value: ReactNode) => void;
    setIsOpen: (value: boolean) => void;
}

export const ModalContext = createContext<ModalContextType>({
    isOpen: false,
    setIsOpen: () => {},
    children: null,
    setChildren: () => {},
})

export interface ModalContextProps
{
    children: ReactNode;
}

const ModalContextProvider: FC<ModalContextProps> = ({ children }) =>
{
    const [isOpenModal, setIsOpenModal] = useState(false);
    const [modalChildren, setModalChildren] = useState<React.ReactNode>(null);

    return <ModalContext.Provider value={{
        isOpen: isOpenModal,
        setIsOpen: setIsOpenModal,
        children: modalChildren,
        setChildren: setModalChildren }}>
        <Modal isOpen={isOpenModal} children={modalChildren} />
        {children}
    </ModalContext.Provider>
};

export default ModalContextProvider;
