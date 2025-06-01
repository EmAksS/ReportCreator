import {FC} from "react";

export interface ButtonProps
{
    onClick: () => void;
    variant: ButtonType;
    type?: string;
    text?: string;
    style?: React.CSSProperties;
    selected?: boolean;
}

export enum ButtonType
{
    general,
    hat,
    toggleable
}

const buttonCSSClasses =
    {
        [ButtonType.general]: "general-button",
        [ButtonType.hat]: "hat-button",
        [ButtonType.toggleable]: "toggleable-button",
    }

const Button: FC<ButtonProps> = (props: ButtonProps) =>
{
    return (
        <button className={`button ${buttonCSSClasses[props.variant]}`}
                onClick={props.onClick}
                style={{...props.style, ...(props.variant === ButtonType.toggleable && {
                        backgroundColor: props.selected ? "whitesmoke" : "white"})}}>
        <p style={{margin: 0}}>{props.text}</p>
        </button>
    )
}

export default Button;