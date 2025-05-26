import React, {CSSProperties, FC, PropsWithChildren, ReactNode} from "react";

export interface ContainerProps
{
    children: ReactNode;
    style?: CSSProperties;
    className?: string;
}

const Container: FC<ContainerProps> = ({style, className, children}) =>
{
    return <div className={"simple-container " + className} style={style}>
        {children}
    </div>;
};

export default Container;
