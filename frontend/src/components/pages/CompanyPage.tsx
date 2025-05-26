import React, {FC, useContext, useEffect, useState} from "react";
import {
    createContractorCompany,
    createContractorPerson,
    createExecutorPerson, getCompany,
    getContractorCompanies,
    getContractorCompanyFields,
    getContractorPersonFields,
    getContractorPersons,
    getExecutorPersonFields,
    getExecutorPersons
} from "../../api/api";
import Form from "../Form";
import {DataValue, Field} from "../../types/api";
import List, {ListItem} from "../List";
import {Company, ContractorCompany, ContractorPerson, ExecutorPerson} from "../../types/core";
import {InputProps} from "../Input";
import {ModalContext} from "../../App";
import SimpleContainer from "../SimpleContainer";

const CompanyPage: FC = () =>
{
    const {
        setIsOpen: setIsOpenModal,
        setChildren: setModalChildren,
    } = useContext(ModalContext);

    const [contractorCompanies, setContractorCompanies] = useState<ContractorCompany[]>([]);
    const [contractorCompanyFields, setContractorCompanyFields] = useState<Field[]>([]);
    const [contractorPersons, setContractorPersons] = useState<ContractorPerson[]>([]);
    const [contractorPersonFields, setContractorPersonFields] = useState<Field[]>([]);

    const [company, setCompany] = useState<Company>();
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
                executorPersonFields,
                contractorCompanies,
                contractorCompanyFields
            ] = await Promise.all([
                getContractorPersons(),
                getExecutorPersons(),
                getContractorPersonFields(),
                getCompany(),
                getExecutorPersonFields(),
                getContractorCompanies(),
                getContractorCompanyFields()
            ]);

            console.log("Юридические лица заказчиков:", contractorPersons);
            setContractorPersons(contractorPersons);

            console.log("Юридические лица исполнителей:", executorPersons);
            setExecutorPersons(executorPersons);

            console.log("Поля юридических лиц заказчиков:", contractorPersonFields);
            setContractorPersonFields(contractorPersonFields);

            console.log("Компания пользователя:", company);
            setCompany(company);

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

    return (<div>
        <h3>О компании</h3>
        {company?.companyFullName}
        <h3>Компании Заказчики</h3>

        <List items={contractorCompanies.map((contractor, index) =>
            ({id: index, content: <div>{contractor.companyFullName}</div>} as ListItem))}
              onAdd={() =>
              {
                  setIsOpenModal(true);
                  setModalChildren(<SimpleContainer><Form submitLabel={"Добавить компанию заказчика"}
                                         inputs={contractorCompanyFields.map(field => ({inputData: field} as InputProps))}
                                         onSubmit={requestCreateContractorCompany}/></SimpleContainer>)
              }}/>

        <h3>Юридические лица заказчиков</h3>

        <List items={contractorPersons.map((person, index) =>
            ({id: index, content: <div>{person.company + " " + person.firstName + " " + person.
                    post}</div>} as ListItem))}
        onAdd={() => {
            setIsOpenModal(true);
            setModalChildren(<SimpleContainer><Form submitLabel={"Добавить юр. лицо заказчика"}
                                   inputs={contractorPersonFields.map(field => ({inputData: field} as InputProps))}
                                   onSubmit={requestCreateContractorPerson}/></SimpleContainer>)
        }}/>

        <h3>Юридические лица исполнителя</h3>

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

    </div>)
}

export default CompanyPage;
