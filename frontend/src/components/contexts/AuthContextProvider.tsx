import React, {createContext, FC, ReactNode, useEffect, useState} from "react";
import {User} from "../../types/core";
import {getUser} from "../../api/api";

export interface AuthContextType
{
    user: User | null;
    isAuthChecked: boolean;
    setUser: (value: User) => void;
    setIsAuthChecked: (value: boolean) => void;
    checkAuth: () => Promise<boolean>;
}

export const AuthContext = createContext<AuthContextType>({
    user: null,
    isAuthChecked: false,
    setUser: () => {},
    setIsAuthChecked: () => {},
    checkAuth: async () => false
});

export interface ModalContextProviderProps
{
    children: ReactNode;
}

const AuthContextProvider: FC<ModalContextProviderProps> = ({children}) =>
{
    const [user, setUser] = useState<User | null>(null);
    const [isAuthChecked, setIsAuthChecked] = useState(false);

    useEffect(() => {
        checkAuth();
    }, []);

    const checkAuth = async (): Promise<boolean> =>
    {
        let requestedUser;
        try
        {
            requestedUser = await getUser();
            setUser(requestedUser);
        }
        catch(e)
        {
            setUser(null);
            setIsAuthChecked(true);
            return false;
        }
        setIsAuthChecked(true);
        return requestedUser !== null;
    };

    return (<AuthContext.Provider value={{ user, setUser, checkAuth, isAuthChecked, setIsAuthChecked }}>
        {children}
    </AuthContext.Provider>)
};

export default AuthContextProvider;
