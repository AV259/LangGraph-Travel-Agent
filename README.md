#  TravelMind AI – Intelligent Multi-Agent Travel Planner

- TravelMind AI is an AI-powered stateful multi-agent travel planning system built using LangGraph and Google Gemini featuring Human-in-the-Loop decision making, tool calling, persistent memory, and real-time API integrations.
The system coordinates specialized AI agents to collaboratively plan complete, personalized travel experiences from destination planning, flight and hotel search, activity recommendations to budget optimization, transportation, and itinerary generation.
---
##  Demo
 - The AI Agent can be accessed here - https://travelmind-ai-agent.streamlit.app/



https://github.com/user-attachments/assets/c00be4e2-40d8-4518-b1e0-7371a96e2cc7


   
##  Features
 - AI Trip Understanding
   - Extracts structured trip details such as destination, dates, budget, duration, departure city, and interests from natural language using Gemini. Automatically identifies missing information for follow-up.
 - Destination Recommendation Agent
   - Recommends personalized destinations based on the traveler's interests, budget, duration, and preferences, along with the nearest airport city and reasoning.
 - Real-Time Flight Search
   - Searches live flight options using Google Flights (SerpAPI) and recommends the best flight based on price, duration, and overall value.
 - Real-Time Hotel Search
   - Retrieves real hotel options from Google Hotels (SerpAPI) and recommends accommodations using price, ratings, amenities, and traveler preferences.
 - Human-in-the-Loop Flight & Hotel Selection
   - Allows travelers to review AI recommendations and manually select their preferred flight and hotel before planning continues.
 - Activity Recommendation Agent
   - Suggests destination-specific attractions and experiences tailored to the traveler's interests using AI reasoning and real-world search results.
 - Restaurant Recommendation Agent
   - Recommends highly rated local restaurants and authentic food experiences, seamlessly integrated into the daily itinerary.
 - Transportation Recommendation Agent
   - Provides transportation suggestions between destinations, including recommended travel modes and estimated travel durations.
 - Budget Optimization
   - Calculates the estimated trip cost by combining flights, hotels, food, transportation, and activities, while tracking the remaining budget.
 - AI Budget Advisor
   - Analyzes the trip budget and intelligently suggests cheaper flight or hotel alternatives when the planned trip exceeds the user's budget.
 - Human-in-the-Loop Budget Decisions
   - Lets travelers choose whether to accept AI recommendations or keep their current selections, with automatic budget recalculation after each decision.
 - Intelligent Itinerary
   - Generates a personalized day-by-day itinerary combining activities, transportation, restaurants, accommodations, and travel tips for a complete travel experience.

## Deployment
 This Agent was deployed as an interactive web application using:
 - Streamlit

##  Tech Stack

### AI & Agent Framework
- LangGraph
- Google Gemini
- Pydantic
- Python

### APIs
- Google Flights (SerpAPI)
- Google Hotels (SerpAPI)
- Google Search (SerpAPI)

### Memory
- ChromaDB

### Database
- SQLite

### Frontend
- Streamlit

### LLM Features
- Structured Outputs
- Tool Calling
- Multi-Agent Workflow
- Human-in-the-Loop
- Memory-Augmented Planning

---

## 📂 Project Structure

```
TravelMind_AI/
│
├── app/
│   ├── agents/
│   ├── graph/
|   ├── memory/
│   ├── state/
│   ├── tools/
│   ├── services/
│   ├── utils/
├── data/
|   ├── airports.csv
├── frontend/
|   ├── streamlit_app.py
├── tests/
├── requirements.txt
└── README.md
```

---

##  Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/TravelMind_AI.git
```

Navigate to the project

```bash
cd TravelMind_AI
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

##  Environment Variables

Create a `.env` file

```text
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
SERP_API_KEY=YOUR_SERPAPI_KEY
```

---

##  Run the Application

```bash
streamlit run streamlit_app.py
```

---

##  Author

**Akash Verma**

M.Sc. Data Science | AI & Machine Learning

GitHub: https://github.com/AV259

LinkedIn: www.linkedin.com/in/akash-verma09

---
