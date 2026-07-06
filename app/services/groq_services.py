from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from app.utils.config import GROQ_API_KEY


groq_client = ChatGroq(
    model="llama3-70b-8192",
    temperature=0.2,
    groq_api_key=GROQ_API_KEY
)


