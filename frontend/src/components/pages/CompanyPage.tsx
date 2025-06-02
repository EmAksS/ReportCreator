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

    return (<div>
        <div style={{display: "flex"}}>
            <SimpleContainer style={{flex: "1"}}>
                <h3 style={{margin: "5px auto"}}>Пользователь</h3>
                {user?.username}
                <h3 style={{margin: "5px auto"}}>Компания</h3>
                {company?.companyFullName}
            </SimpleContainer>

            <SimpleContainer style={{flex: "1"}}>
                <h3 style={{margin: "5px auto"}}>Пользователи компании</h3>
                <List hideRemoveButtons={true} items={companyUsers.map((currentUser, index) =>
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

                <List hideRemoveButtons={true} items={contractorCompanies.map((contractor, index) =>
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
                <List hideRemoveButtons={true} items={contractorPersons.map((person, index) =>
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

                <List hideRemoveButtons={true} items={executorPersons.map((person, index) =>
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
