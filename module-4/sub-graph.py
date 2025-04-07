from typing_extensions import TypedDict
from typing import List, Annotated, Optional
from dotenv import load_dotenv


load_dotenv()

class Log(TypedDict):
    id:str,