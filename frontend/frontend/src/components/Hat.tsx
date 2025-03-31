import {FC} from "react";
import Button, {ButtonProps} from "./Button";

export interface HatProps
{
    title?: string;
    imageSrc: string;
    buttonProps: ButtonProps[];
}

const Hat: FC<HatProps> = (props: HatProps) =>
{
    return (
        <div className={"hat"}>
            <img className={"hat-logo"} src={props.imageSrc} alt={""}></img>
            <h1 className="hat_title">{props.title}</h1>
            {props.buttonProps.map((props) =>
            {
                return (<Button key={props.text} {...props} ></Button>)
            })}
        </div>
    );
}

export default Hat;