from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal
from datetime import date, datetime
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import streamlit as st

try:
    load_dotenv('HUGGINGFACE_API_TOKEN')
    HUGGINGFACE_API_TOKEN = os.getenv('HUGGINGFACE_API_TOKEN')
except Exception as e:
    HUGGINGFACE_API_TOKEN = st.secrets["HUGGINGFACE_API_TOKEN"]
    os.environ["FIREWORKS_API_KEY"] = st.secrets["FIREWORKS_API_KEY"]
    os.environ["HUGGINGFACE_API_TOKEN"] = st.secrets["HUGGINGFACE_API_TOKEN"]


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

class Investment:
    def __init__(self):
        pass

    def checkAge(self, state: Person) -> Person:
        state['age'] = (datetime.today().date() - state['dob']).days // 365
        return state

    def conditionCapital(self, state: Person) -> str:
        if state['capital'] > 100000:
            return 'High'
        else:
            return 'Low'

    def getHighInvestmentScale(self, state: Person) -> Person:
        state['scale_business'] = 'High'
        return state

    def getLowInvestmentScale(self, state: Person) -> Person:
        state['scale_business'] = 'Low'
        return state

    def conditionService(self, state: Person) -> str:
        return state['interest']

    def getServiceBusinessName(self, state: Person) -> Person:
        state['business_name'] = 'Pilas Services'
        return state

    def getManufacturingBusinessName(self, state: Person) -> Person:
        state['business_name'] = 'Pilas Manufacturing'
        return state

    def getBusinessCase(self, state: Person) -> Person:
        llm = HuggingFaceEndpoint(repo_id='deepseek-ai/DeepSeek-R1', temperature=0.3,
                                  task='text-generation', verbose=False,
        huggingfacehub_api_token = HUGGINGFACE_API_TOKEN )

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

    def make_builder(self):
        builder = StateGraph(Person)

        builder.add_node('check_age', self.checkAge)
        builder.add_node('get_high_scale', self.getHighInvestmentScale)
        builder.add_node('get_low_scale', self.getLowInvestmentScale)
        builder.add_node('get_service_bn', self.getServiceBusinessName)
        builder.add_node('get_manufacturing_bn', self.getManufacturingBusinessName)
        builder.add_node('get_business_case', self.getBusinessCase)


        builder.add_edge(START, 'check_age')
        builder.add_conditional_edges('check_age', self.conditionCapital, {'High': 'get_high_scale', 'Low': 'get_low_scale'})
        builder.add_conditional_edges('get_high_scale', self.conditionService, {'Service': 'get_service_bn', 'Manufacturing': 'get_manufacturing_bn' } )
        builder.add_conditional_edges('get_low_scale', self.conditionService, {'Service': 'get_service_bn', 'Manufacturing': 'get_manufacturing_bn' } )
        builder.add_edge('get_service_bn', 'get_business_case' )
        builder.add_edge('get_manufacturing_bn', 'get_business_case' )

        builder.add_edge('get_business_case', END)

        graph = builder.compile()

        return graph



if __name__ == '__main__':
    myInvestment = Investment()
    graph = myInvestment.make_builder()
    object_update = graph.invoke({'name': 'samuel', 'dob' : datetime.strptime('21-may-1989', "%d-%b-%Y"), 'capital':2300, 'country':'Ghana', 'interest': 'Service'})
    print(object_update)
    print(graph.get_graph().draw_ascii())