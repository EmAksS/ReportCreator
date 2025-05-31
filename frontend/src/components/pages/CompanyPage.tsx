import React, {FC, useContext, useEffect, useState} from "react";
import {
    createContractorCompany,
    createContractorPerson,
    createExecutorPerson, createUser, getCompany, getCompanyUsers,
    getContractorCompanies,
    getContractorCompanyFields,
    getContractorPersonFields,
    getContractorPersons,
    getExecutorPersonFields,
    getExecutorPersons, getUserRegistrationFields
} from "../../api/api";
import Form from "../Form";
import {DataValue, Field} from "../../types/api";
import List, {ListItem} from "../List";
import {Company, ContractorCompany, ContractorPerson, ExecutorPerson, User} from "../../types/core";
import {InputProps} from "../Input";
import SimpleContainer from "../SimpleContainer";
import {AuthContext} from "../contexts/AuthContextProvider";
import {ModalContext} from "../contexts/ModalContextProvider";

const CompanyPage: FC = () =>
{
    const { user } = useContext(AuthContext);
    const {
        setIsOpen: setIsOpenModal,
        setChildren: setModalChildren,
    } = useContext(ModalContext);

    const [contractorCompanies, setContractorCompanies] = useState<ContractorCompany[]>([]);
    const [contractorCompanyFields, setContractorCompanyFields] = useState<Field[]>([]);
    const [contractorPersons, setContractorPersons] = useState<ContractorPerson[]>([]);
    const [contractorPersonFields, setContractorPersonFields] = useState<Field[]>([]);

    const [company, setCompany] = useState<Company>();
    const [companyUsers, setCompanyUsers] = useState<User[]>([]);
    const [companyUserFields, setCompanyUserFields] = useState<Field[]>([]);
    const [executorPersons, setExecutorPersons] = useState<ExecutorPerson[]>([]);
    const [executorPersonFields, setExecutorPersonFields] = useState<Field[]>([]);

    useEffect(() => {
        reloadData()
    }, []);

    const reloadData = async () => {
        try {
            const [
                contractorPersons,
                executorPersons,
                contractorPersonFields,
                company,
                companyUsers,
                executorPersonFields,
                contractorCompanies,
                contractorCompanyFields
            ] = await Promise.all([
                getContractorPersons(),
                getExecutorPersons(),
                getContractorPersonFields(),
                getCompany(),
                getCompanyUsers(),
                getExecutorPersonFields(),
                getContractorCompanies(),
                getContractorCompanyFields()
            ]);

            let companyUserFields: Field[] = [];
            if (user?.isCompanySuperuser)
            {
                companyUserFields = await getUserRegistrationFields();
            }

            console.log("Юридические лица заказчиков:", contractorPersons);
            setContractorPersons(contractorPersons);

            console.log("Юридические лица исполнителей:", executorPersons);
            setExecutorPersons(executorPersons);

            console.log("Поля юридических лиц заказчиков:", contractorPersonFields);
            setContractorPersonFields(contractorPersonFields);

            console.log("Компания пользователя:", company);
            setCompany(company);

            console.log("Пользователи компании:", company);
            setCompanyUsers(companyUsers)

            console.log("Поля для создания пользователя в компании:", companyUserFields);
            setCompanyUserFields(companyUserFields)

            console.log("Поля юридических лиц исполнителей:", executorPersonFields);
            setExecutorPersonFields(executorPersonFields);

            console.log("Компании заказчики:", contractorCompanies);
            setContractorCompanies(contractorCompanies);

            console.log("Поля компаний заказчиков:", contractorCompanyFields);
            setContractorCompanyFields(contractorCompanyFields);
        }
        catch (error)
        {
            console.error("Ошибка при загрузке данных:", error);
        }
    };

    const requestCreateExecutorPerson = async (values: DataValue[]) =>
    {
        console.log("пытаемся создать лицо исполнителя");
        const response = await createExecutorPerson(values);
        console.log(response);
        setExecutorPersons(await getExecutorPersons());
    }

    const requestCreateContractorPerson = async (values: DataValue[]) =>
    {
        console.log("пытаемся создать лицо заказчика");
        const response = await createContractorPerson(values);
        console.log(response);
        setContractorPersons(await getContractorPersons());
    }

    const requestCreateContractorCompany = async (values: DataValue[]) =>
    {
        console.log("пытаемся создать компанию заказчика");
        const response = await createContractorCompany(values);
        console.log(response);
        setContractorCompanies(await getContractorCompanies());
    }

    const requestCreateCompanyUser = async (values: DataValue[]) =>
    {
        console.log("пытаемся создать пользователя");
        const response = await createUser(values);
        console.log(response);
        setCompanyUsers(await getCompanyUsers());
    }

    return (<div>
        <SimpleContainer style={{width: "fit-content"}}>
            <h3 style={{margin: "5px auto"}}>Я</h3>
            {user?.username}
        </SimpleContainer>

        <SimpleContainer style={{width: "fit-content"}}>
            <h3 style={{margin: "5px auto"}}>О компании</h3>
            {company?.companyFullName}
        </SimpleContainer>
        <SimpleContainer style={{width: "fit-content"}}>
            <h3 style={{margin: "5px auto"}}>Пользователи компании</h3>
            <List items={companyUsers.map((currentUser, index) =>
                ({id: index, content: <div>{(user?.username == currentUser.username ? "Вы: " : "") + currentUser.username + " " + (currentUser.isCompanySuperuser ? "👑" : "")}</div>} as ListItem))}
                  onAdd={() =>
                  {
                      if (user?.isCompanySuperuser)
                      {
                          setIsOpenModal(true);
                          setModalChildren(<SimpleContainer><Form submitLabel={"Добавить пользователя"}
                                                                  inputs={companyUserFields.map(field => ({inputData: field} as InputProps))}
                                                                  onSubmit={requestCreateCompanyUser}/></SimpleContainer>)
                      }
                  }}/>
        </SimpleContainer>
        <SimpleContainer style={{width: "fit-content"}}>
            <h3 style={{margin: "5px auto"}}>Компании Заказчики</h3>

            <List items={contractorCompanies.map((contractor, index) =>
                ({id: index, content: <div>{contractor.companyFullName + " " + contractor.contractorCity}</div>} as ListItem))}
                  onAdd={() =>
                  {
                      setIsOpenModal(true);
                      setModalChildren(<SimpleContainer><Form submitLabel={"Добавить компанию заказчика"}
                                             inputs={contractorCompanyFields.map(field => ({inputData: field} as InputProps))}
                                             onSubmit={requestCreateContractorCompany}/></SimpleContainer>)
                  }}/>
        </SimpleContainer>

        <SimpleContainer style={{width: "fit-content"}}>
            <h3 style={{margin: "5px auto"}}>Юридические лица заказчиков</h3>
                <List items={contractorPersons.map((person, index) =>
                    ({id: index, content: <div>{person.company + " " + person.firstName + " " + person.
                            post + " " + person.surname + " " + person.lastName}</div>} as ListItem))}
                onAdd={() => {
                    setIsOpenModal(true);
                    setModalChildren(<SimpleContainer><Form submitLabel={"Добавить юр. лицо заказчика"}
                                           inputs={contractorPersonFields.map(field => ({inputData: field} as InputProps))}
                                           onSubmit={requestCreateContractorPerson}/></SimpleContainer>)
                }}/>
        </SimpleContainer>

        <SimpleContainer style={{width: "fit-content"}}>
            <h3 style={{margin: "5px auto"}}>Юридические лица исполнителя</h3>

            <List items={executorPersons.map((person, index) =>
                ({id: index, content: <div>{person.post + " " + person.firstName}</div>} as ListItem))}
                  onAdd={() => {
                      setIsOpenModal(true);
                      setModalChildren(<SimpleContainer>
                          <Form submitLabel={"Добавить юр. лицо исполнителя"}
                                inputs={executorPersonFields.map(field => ({inputData: field} as InputProps))}
                                onSubmit={requestCreateExecutorPerson}/>
                      </SimpleContainer>)
                  }}/>
        </SimpleContainer>
    </div>)
}

export default CompanyPage;
