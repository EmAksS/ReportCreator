import React, {FC, useEffect, useState} from "react";

const WelcomePage: FC = () =>
{
    const [userName, setUserName] = useState<string>("");

    useEffect(() => {

    }, []);

    return (<div>{"Добро пожаловать "}</div>)
}

export default WelcomePage;
