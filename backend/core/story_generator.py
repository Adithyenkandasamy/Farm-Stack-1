from sqlalchemy.orm import Session
from core.config import Settings

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from core.prompts import STORY_PROMPT
from models.story import Story