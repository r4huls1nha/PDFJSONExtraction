import os
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import OutputFixingParser
from langchain.schema import OutputParserException
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List
from langchain.document_loaders import PyPDFLoader
import json

openai_api_key = '#'

# Define a new Pydantic model with field descriptions and tailored for Twitter.
class Company(BaseModel):
    CompanyName: str = Field(description="Full name of the company.")
    Description: str = Field(description="Summary of the company in their own words")
    BusinessModel: int = Field(description="B2B or B2C or B2G or B2B2C, or any other variation? State in the B2x format.")
    Sectors: List[str] = Field(description="List of sectors the company operates in.") #amend this to include CP parameters
    Email: str = Field(description="Email address of the company. In the form - x@y.com. Usually in the final page.")
    FundraiseAmount: str = Field(description="Amount of money being raised. Usually in pound sterling - £x. Will be in past tense - may mention EIS or SEIS, and state if they do.")
    AmountRaised: str = Field(description="Amount of money already pleged. In GBP, pound sterling, £, or another currency. Will be in past tense.")
    Location: str = Field(description="A geographical location where the company is based. Could be stated as a region or an address. The more regionally precise the better. Usually in final page.")
    DevelopmentStage: str = Field(description= "Do they have a full product, an MVP, or are they in the ideation phase?")
    RevenueStage: str = Field(description="Are they pre-revenue, in the early revenue stages, or do they have monthly recurring revenue?")


    # Instantiate the parser with the new model.
parser = PydanticOutputParser(pydantic_object=Company)

# Update the prompt to match the new query and desired format.
prompt = ChatPromptTemplate(
    messages=[
        HumanMessagePromptTemplate.from_template(
            "answer the users question as best as possible. State the sources you pulled from. Explain step by step the reasoning. Don't just look at any one point of the deck, look at all points - don't expect all the info to be in one place.\n{format_instructions}\n{question}"
        )
    ],
    input_variables=["question"],
    partial_variables={
        "format_instructions": parser.get_format_instructions(),
    },
)
chat_model = ChatOpenAI(
    model="gpt-4",
    openai_api_key=openai_api_key,
    max_tokens=1000
)

loader = PyPDFLoader("deck.pdf")
document = loader.load()

document_query = "Create a profile based on this description: " + document[0].page_content

_input = prompt.format_prompt(question=document_query)
output = chat_model(_input.to_messages())
parsed = parser.parse(output.content)

try:
    parsed = parser.parse(output.content)
    parsed = json.dumps(parsed.dict())
except OutputParserException as e:
    new_parser = OutputFixingParser.from_llm(
        parser=parser,
        llm=ChatOpenAI()
    )
    parsed = new_parser.parse(output.content)

print(parsed)
