import {FC} from "react";
import Button, {ButtonProps} from "./Button";
import {useLocation, useNavigate} from "react-router-dom";
import {ROUTES} from "../App";

export interface HatProps
{
    title?: string;
    imageSrc?: string;
    buttonProps?: ButtonProps[];
    children?: React.ReactNode;
    onLogoClick?: () => void;
}

const Hat: FC<HatProps> = (props: HatProps) =>
{
    return (
        <div className={"hat"}>
            <img className={"hat-logo"} style={{cursor: "pointer"}} src={props.imageSrc} alt={""} onClick={props.onLogoClick}></img>
            <h1 className="hat_title" style={{cursor: "pointer"}} onClick={props.onLogoClick}>{props.title}</h1>
            {props.children}
            {props.buttonProps?.map((props) =>
            {
                return (<Button key={props.text} {...props} ></Button>)
            })}
        </div>
    );
}

export default Hat;