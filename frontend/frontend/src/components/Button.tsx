import {FC} from "react";

export interface ButtonProps
{
    onClick: () => void;
    variant: ButtonType;
    text?: string;
    style?: React.CSSProperties;
}

export enum ButtonType
{
    general,
    hat
}

const buttonCSSClasses =
    {
        [ButtonType.general]: "general-button",
        [ButtonType.hat]: "hat-button",
    }

const Button: FC<ButtonProps> = (props: ButtonProps) =>
{
    return (
        <button className={`button ${buttonCSSClasses[props.variant]}`}
                onClick={props.onClick}
                style={props.style}>
            <p style={{margin: 0}}>{props.text}</p>
        </button>
    )
}

export default Button;