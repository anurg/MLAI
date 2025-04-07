from typing import TypedDict,List,Optional,Annotated
from dotenv import load_dotenv


load_dotenv()

class Log(TypedDict):
    id:str,