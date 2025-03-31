import {FC} from "react";
import {ButtonProps} from "./Button";

const HatButton: FC<ButtonProps> = (props: ButtonProps) =>
{
    return (
        <button className={"button"}
                onClick={props.onClick}
                style={props.style ? props.style : {}}>

            <h3 style={{margin: 0}}>{props.text}</h3>
        </button>
    )
}

export default HatButton;