# ✈️ TravelMind — AI-Powered Travel Planning Agent

**Plan smarter. Explore better. Travel with intelligence.**

TravelMind is a full-stack, AI-powered travel planning application built using a **ReAct (Reasoning + Acting) agent**. It generates personalized travel itineraries by combining real-world tourist attraction data, date-specific weather forecasts, and budget calculations.

Unlike a basic chatbot that relies only on generated text, TravelMind can dynamically select and execute external tools to support its recommendations.

## 🌟 Key Features

- **AI-Powered Itinerary Generation:** Personalized day-wise plans based on destination, travel dates, duration, budget, and interests.
- **ReAct Agent Architecture:** Dynamic tool selection, execution, observation, and response generation.
- **Weather-Aware Planning:** Date-specific forecasts help the agent recommend suitable activities.
- **Real Tourist Attractions:** Discovers places of interest using the OpenTripMap API.
- **Smart Budget Planner:** Calculates total estimated expenses, remaining budget, and overspending alerts.
- **Interactive Frontend:** Responsive React interface with a visual budget breakdown.
- **Tool Execution Visibility:** Displays the tools invoked during itinerary generation.

## 🧠 Why TravelMind Is a ReAct Agent

**ReAct stands for Reasoning and Acting.**

TravelMind uses an LLM-powered agent that can decide which tools to call based on the user's request.

### Agent Workflow

```text
             USER REQUEST
                  |
                  v
          REACT AI AGENT
          (Gemini + LangChain)
                  |
                  v
       REASON ABOUT THE TASK
                  |
                  v
         SELECT AND CALL TOOLS
                  |
       +----------+----------+
       |          |          |
       v          v          v
    Weather    Attractions  Budget
    Forecast     Finder    Calculator
       |          |          |
       +----------+----------+
                  |
                  v
          OBSERVE TOOL RESULTS
                  |
                  v
        REASON AND SYNTHESIZE
                  |
                  v
       PERSONALIZED ITINERARY
```

### How It Works

1. **Reason:** The agent interprets the user's destination, dates, budget, and interests.
2. **Act:** It selects and executes the appropriate tools.
3. **Observe:** It receives weather, attraction, and budget information.
4. **Repeat if necessary:** It can perform additional tool calls.
5. **Respond:** It generates a structured, personalized travel itinerary.

The agent's tool-selection process is dynamic rather than a completely hardcoded sequence.

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| Frontend | React, JavaScript, CSS, Vite |
| Backend | Python, FastAPI, Uvicorn |
| AI Model | Google Gemini |
| Agent Framework | LangChain, LangGraph |
| Weather Data | Open-Meteo API |
| Attraction Data | OpenTripMap API |
| Budget Calculation | Custom Python tool |
| API Communication | REST API, JSON |

## 🔧 AI Tools

### 1. `get_weather_forecast`

- Geocodes the destination.
- Retrieves date-specific weather information from Open-Meteo.
- Returns temperature, weather conditions, and precipitation probability.
- Reports when requested dates fall outside the supported forecast window.

### 2. `find_tourist_attractions`

- Retrieves destination coordinates.
- Searches for nearby tourist attractions using OpenTripMap.
- Filters unnamed and duplicate locations.
- Provides real attraction data to the agent.

### 3. `calculate_trip_budget`

- Processes user-provided expense estimates.
- Calculates total expenses and remaining budget.
- Identifies whether estimated spending exceeds the budget.

**Note:** Budget calculations use user-provided estimates, not live hotel or flight prices.

## 🏗️ Project Structure

```text
TravelMind/
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── agent.py
│   ├── tools.py
│   └── schemas.py
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── services/
│   │       └── api.js
│   ├── package.json
│   └── vite.config.js
├── .gitignore
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3
- Node.js and npm
- Google Gemini API key
- OpenTripMap API key

### 1. Clone the Repository

```bash
git clone https://github.com/sampadabhagat15-sys/TravelMind.git
cd TravelMind
```

### 2. Set Up the Backend

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key
OPENTRIPMAP_API_KEY=your_opentripmap_api_key
```

Start the FastAPI backend:

```bash
uvicorn backend.main:app --reload --port 8001
```

Backend: `http://127.0.0.1:8001`

API documentation: `http://127.0.0.1:8001/docs`

### 3. Set Up the Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend: `http://localhost:5173`

### 4. Generate Your First Itinerary

1. Enter a destination.
2. Select your travel date and duration.
3. Enter your budget and interests.
4. Optionally provide estimated expenses.
5. Click **Generate My Itinerary**.
6. Explore your weather-aware itinerary and agent tool execution details.

## 🔌 API Overview

### `POST /plan`

Example request:

```json
{
  "message": "Plan a 3-day trip to Mysuru starting on 2026-11-25. My budget is INR 10000. I enjoy history and museums."
}
```

The backend returns a JSON response containing the generated itinerary and the names of tools used.

### `GET /`

Returns the backend service status.

## 📸 Screenshots

Screenshots of the homepage, trip planner, generated itinerary, and AI tool execution can be added here.

## ⚠️ Current Limitations

- Weather forecasts are limited to the API's supported forecast window.
- Budget calculations rely on user-provided estimates.
- Attraction opening hours, prices, and travel times are not independently verified.
- Hotel and flight booking are not supported.
- Persistent trip history and user authentication are not yet implemented.
- The application requires internet connectivity and external API availability.

## 🔮 Future Enhancements

- Interactive maps and route optimization.
- Live hotel and flight pricing.
- Booking integrations.
- User accounts and saved itineraries.
- Downloadable PDF travel plans.
- More advanced travel recommendations.

## 👩‍💻 Developer

**Sampada Bhagat**

Computer Science & Engineering Student

GitHub: [@sampadabhagat15-sys](https://github.com/sampadabhagat15-sys)

Project Repository: [TravelMind](https://github.com/sampadabhagat15-sys/TravelMind)

---

**TravelMind demonstrates how Agentic AI can combine language-model reasoning, external tools, and full-stack development to solve a practical travel planning problem.**