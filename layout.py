from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal
from datetime import date, datetime
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os


load_dotenv('HUGGINGFACE_API_TOKEN')
HUGGINGFACE_API_TOKEN = os.getenv('HUGGINGFACE_API_TOKEN')

class Person(TypedDict, total=False):
    name: str
    dob: date
    age: int
    country: Literal['Ghana', 'Germany']
    capital: float
    scale_business : Literal['High', 'Low']
    interest: Literal['Service', 'Manufacturing']
    business_name : str
    business_case: str

def checkAge(state: Person) -> Person:
    state['age'] = (datetime.today() - state['dob']).days // 365
    return state

def conditionCapital(state: Person) -> str:
    if state['capital'] > 100000:
        return 'High'
    else:
        return 'Low'

def getHighInvestmentScale(state: Person) -> Person:
    state['scale_business'] = 'High'
    return state

def getLowInvestmentScale(state: Person) -> Person:
    state['scale_business'] = 'Low'
    return state

def conditionService(state: Person) -> str:
    return state['interest']

def getServiceBusinessName(state: Person) -> Person:
    state['business_name'] = 'Pilas Services'
    return state

def getManufacturingBusinessName(state: Person) -> Person:
    state['business_name'] = 'Pilas Manufacturing'
    return state

def getBusinessCase(state: Person) -> Person:
    llm = HuggingFaceEndpoint(repo_id='deepseek-ai/DeepSeek-R1', temperature=0.3,
                              task='text-generation', verbose=False)

    chat_model = ChatHuggingFace(llm=llm)

    template = '''Hi, my name is {name}, and i am {age} old, i want to start a {scale} business in {country} 
                    with a capital of {capital} in the {interest} industry. in a simple step, give me a business case
                    for this business. Make it a very short business case.                
                '''
    prompt = PromptTemplate(input_variables=['name', 'age', 'scale', 'country', 'capital', 'interest'], template=template)

    chain = prompt | chat_model

    response = chain.invoke({'name': state['name'], 'age': state['age'], 'scale': state['scale_business'],
                             'country': state['country'], 'capital': state['capital'],
                             'interest': state['interest']})
    state['business_case'] = response.content
    return state


builder = StateGraph(Person)

builder.add_node('check_age', checkAge)
builder.add_node('get_high_scale', getHighInvestmentScale)
builder.add_node('get_low_scale', getLowInvestmentScale)
builder.add_node('get_service_bn', getServiceBusinessName)
builder.add_node('get_manufacturing_bn', getManufacturingBusinessName)
builder.add_node('get_business_case', getBusinessCase)


builder.add_edge(START, 'check_age')
builder.add_conditional_edges('check_age', conditionCapital, {'High': 'get_high_scale', 'Low': 'get_low_scale'})
builder.add_conditional_edges('get_high_scale', conditionService, {'Service': 'get_service_bn', 'Manufacturing': 'get_manufacturing_bn' } )
builder.add_conditional_edges('get_low_scale', conditionService, {'Service': 'get_service_bn', 'Manufacturing': 'get_manufacturing_bn' } )
builder.add_edge('get_service_bn', 'get_business_case' )
builder.add_edge('get_manufacturing_bn', 'get_business_case' )

builder.add_edge('get_business_case', END)

graph = builder.compile()



if __name__ == '__main__':
    object_update = graph.invoke({'name': 'samuel', 'dob' : datetime.strptime('21-may-1989', "%d-%b-%Y"), 'capital':2300, 'country':'Ghana', 'interest': 'Service'})
    print(object_update)
    print(graph.get_graph().draw_ascii())