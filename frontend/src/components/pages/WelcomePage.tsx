import React, {FC, useEffect, useState} from "react";
import TableInput from "../inputs/TableInput";
import {Field, InputType, TableField, TextField} from "../../types/api";

const WelcomePage: FC = () =>
{
    const [userName, setUserName] = useState<string>("");

    useEffect(() => {

    }, []);

    return (<div style={{padding: "100px"}}></div>)
}

export default WelcomePage;
