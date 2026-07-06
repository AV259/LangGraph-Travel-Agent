from langchain_google_genai import ChatGoogleGenerativeAI
from app.utils.config import GOOGLE_API_KEY

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.3
)

'''Testing the connection to the Gemini API
def test_connection():
    response = llm.invoke("Say hello")
    return response.content
'''