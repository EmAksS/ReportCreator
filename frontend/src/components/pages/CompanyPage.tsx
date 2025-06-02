import React, {FC, use, useContext, useEffect, useState} from "react";
import {
    createContractorCompany,
    createContractorPerson,
    createExecutorPerson,
    createUser,
    deleteCompany, deleteCompanyUser, deleteContractorCompany, deleteContractorPerson, deleteExecutorPerson,
    getCompany,
    getCompanyUsers,
    getContractorCompanies,
    getContractorCompanyFields,
    getContractorPersonFields,
    getContractorPersons,
    getExecutorPersonFields,
    getExecutorPersons,
    getUserRegistrationFields
} from "../../api/api";
import Form from "../Form";
import {DataValue, Field} from "../../types/api";
import List, {ListItem} from "../List";
import {Company, ContractorCompany, ContractorPerson, ExecutorPerson, User} from "../../types/core";
import {InputProps} from "../Input";
import SimpleContainer from "../SimpleContainer";
import {AuthContext} from "../contexts/AuthContextProvider";
import {ModalContext} from "../contexts/ModalContextProvider";
import Button, {ButtonType} from "../Button";

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

            setContractorPersons(contractorPersons);
            setExecutorPersons(executorPersons);
            setContractorPersonFields(contractorPersonFields);
            setCompany(company);
            setCompanyUsers(companyUsers)
            setCompanyUserFields(companyUserFields)
            setExecutorPersonFields(executorPersonFields);
            setContractorCompanies(contractorCompanies);
            setContractorCompanyFields(contractorCompanyFields);
        }
        catch (error)
        {
            console.error("Ошибка при загрузке данных:", error);
        }
    };

    const requestCreateExecutorPerson = async (values: DataValue[]) =>
    {
        await createExecutorPerson(values);
        setExecutorPersons(await getExecutorPersons());
    }

    const requestCreateContractorPerson = async (values: DataValue[]) =>
    {
        await createContractorPerson(values);
        setContractorPersons(await getContractorPersons());
    }

    const requestCreateContractorCompany = async (values: DataValue[]) =>
    {
        await createContractorCompany(values);
        setContractorCompanies(await getContractorCompanies());
    }

    const requestCreateCompanyUser = async (values: DataValue[]) =>
    {
        await createUser(values);
        setCompanyUsers(await getCompanyUsers());
    }

    const requestDeleteCompany = async () =>
    {
        if (user?.isCompanySuperuser)
        {
            setIsOpenModal(true)
            setModalChildren(
                <SimpleContainer>
                    <p>Вы уверены, что хотите удалить компанию?</p>
                    <Button text={"Да"} variant={ButtonType.general} onClick={async () => await deleteCompany()} style={{width: "100%"}} />
                </SimpleContainer>)
        }
    }

    const requestDeleteContractorCompany = async (company: ContractorCompany) =>
    {
        setIsOpenModal(true)
        setModalChildren(
            <SimpleContainer>
                <p>Вы уверены, что хотите удалить компанию заказчика {company.companyFullName}?</p>
                <Button text={"Да"} variant={ButtonType.general} onClick={async () => {
                    await deleteContractorCompany(company.id)
                    setContractorCompanies(await getContractorCompanies())
                    setContractorPersons(await getContractorPersons());
                    setIsOpenModal(false)
                }} style={{width: "100%"}} />
            </SimpleContainer>)
    }

    const requestDeleteContractorPerson = async (person: ContractorPerson) =>
    {
        setIsOpenModal(true)
        setModalChildren(
            <SimpleContainer>
                <p>Вы уверены, что хотите удалить юр. лицо компании заказчика "{person.firstName} {person.lastName} {person.surname}"?</p>
                <Button text={"Да"} variant={ButtonType.general} onClick={async () => {
                    await deleteContractorPerson(person.id)
                    setContractorPersons(await getContractorPersons());
                    setIsOpenModal(false)
                }} style={{width: "100%"}} />
            </SimpleContainer>)
    }

    const requestDeleteExecutorPerson = async (person: ExecutorPerson) =>
    {
        setIsOpenModal(true)
        setModalChildren(
            <SimpleContainer>
                <p>Вы уверены, что хотите удалить юр. лицо исполнителя "{person.firstName} {person.lastName} {person.surname}"?</p>
                <Button text={"Да"} variant={ButtonType.general} onClick={async () => {
                    await deleteExecutorPerson(person.id)
                    setExecutorPersons(await getExecutorPersons());
                    setIsOpenModal(false)
                }} style={{width: "100%"}} />
            </SimpleContainer>)
    }

    const requestDeleteCompanyUser = async (username: string) =>
    {
        if (user?.isCompanySuperuser && user.username !== username)
        {
            setIsOpenModal(true)
            setModalChildren(
                <SimpleContainer>
                    <p>Вы уверены, что хотите удалить пользователя {username}?</p>
                    <Button text={"Да"} variant={ButtonType.general} onClick={async () => {
                        await deleteCompanyUser(username);
                        setCompanyUsers(await getCompanyUsers());
                        setIsOpenModal(false)
                    } } style={{width: "100%"}} />
                </SimpleContainer>)
        }
    }

    return (<div>
        <div style={{display: "flex"}}>
            <SimpleContainer style={{flex: "1"}}>
                <h3 style={{margin: "5px auto"}}>Пользователь</h3>
                {user?.username}
                <h3 style={{margin: "5px auto"}}>Компания</h3>
                <List hideAddButton={true} hideRemoveButtons={!user?.isCompanySuperuser} items={[{content: <span>{company?.companyFullName}</span>, id: 0} as ListItem]} onRemove={() => requestDeleteCompany()} />
            </SimpleContainer>

            <SimpleContainer style={{flex: "1"}}>
                <h3 style={{margin: "5px auto"}}>Пользователи компании</h3>
                <List onRemove={(id) => requestDeleteCompanyUser(companyUsers[id].username)} hideRemoveButtons={!user?.isCompanySuperuser} items={companyUsers.map((currentUser, index) =>
                    ({id: index, content: <div>{(user?.username == currentUser.username ? "Вы: " : "") + currentUser.username + " " + (currentUser.isCompanySuperuser ? "👑" : "")}</div>} as ListItem))}
                      onAdd={() =>
                      {
                          if (user?.isCompanySuperuser)
                          {
                              setIsOpenModal(true);
                              setModalChildren(<SimpleContainer style={{width: "500px"}}><Form submitLabel={"Добавить пользователя"}
                                                                      inputs={companyUserFields.map(field => ({inputData: field} as InputProps))}
                                                                      onSubmit={requestCreateCompanyUser}/></SimpleContainer>)
                          }
                      }}/>
            </SimpleContainer>
        </div>

        <div style={{display: "flex"}}>
            <SimpleContainer style={{flex: "1"}}>
                <h3 style={{margin: "5px auto"}}>Компании Заказчики</h3>

                <List onRemove={(id) => requestDeleteContractorCompany(contractorCompanies[id])} items={contractorCompanies.map((contractor, index) =>
                    ({id: index, content: <div>{contractor.companyFullName}</div>} as ListItem))}
                      onAdd={() =>
                      {
                          setIsOpenModal(true);
                          setModalChildren(<SimpleContainer style={{width: "500px"}}><Form submitLabel={"Добавить компанию заказчика"}
                                                                  inputs={contractorCompanyFields.map(field => ({inputData: field} as InputProps))}
                                                                  onSubmit={requestCreateContractorCompany}/></SimpleContainer>)
                      }}/>
            </SimpleContainer>

            <SimpleContainer style={{flex: "1"}}>
                <h3 style={{margin: "5px auto"}}>Юридические лица заказчиков</h3>
                <List onRemove={(id) => requestDeleteContractorPerson(contractorPersons[id])} items={contractorPersons.map((person, index) =>
                    ({id: index, content: <div>{person.personType + " " + person.post + " " + person.
                            lastName + " " + person.firstName + " " + person.surname}</div>} as ListItem))}
                      onAdd={() => {
                          setIsOpenModal(true);
                          setModalChildren(<SimpleContainer style={{width: "500px"}}><Form submitLabel={"Добавить юр. лицо заказчика"}
                                                                  inputs={contractorPersonFields.map(field => ({inputData: field} as InputProps))}
                                                                  onSubmit={requestCreateContractorPerson}/></SimpleContainer>)
                      }}/>
            </SimpleContainer>

            <SimpleContainer style={{flex: "1"}}>
                <h3 style={{margin: "5px auto"}}>Юридические лица исполнителя</h3>

                <List onRemove={(id) => requestDeleteExecutorPerson(executorPersons[id])} items={executorPersons.map((person, index) =>
                    ({id: index, content: <div>{person.personType + " " + person.post + " " + person.
                            lastName + " " + person.firstName + " " + person.surname}</div>} as ListItem))}
                      onAdd={() => {
                          setIsOpenModal(true);
                          setModalChildren(<SimpleContainer style={{width: "500px"}}>
                              <Form submitLabel={"Добавить юр. лицо исполнителя"}
                                    inputs={executorPersonFields.map(field => ({inputData: field} as InputProps))}
                                    onSubmit={requestCreateExecutorPerson}/>
                          </SimpleContainer>)
                      }}/>
            </SimpleContainer>
        </div>
    </div>)
}

export default CompanyPage;
