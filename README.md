# ✈️ TravelMind — AI-Powered Travel Planning Agent

### Plan Smarter. Explore Better. Travel with Intelligence.

**TravelMind** is a full-stack, AI-powered travel planning application built using **ReAct (Reasoning + Acting) agent architecture**, Google Gemini, LangChain, React and FastAPI.

It generates personalized travel itineraries by integrating real-world tourist attractions, weather forecasts and intelligent budget calculations.

Unlike a traditional AI chatbot, TravelMind can **autonomously select and execute external tools**, observe their results and generate context-aware travel recommendations.

### 🌐 [Launch Live Application](https://travel-mind-beta.vercel.app)

[![Live Demo](https://img.shields.io/badge/Live_Demo-Vercel-000000?style=for-the-badge&logo=vercel)](https://travel-mind-beta.vercel.app)
[![Backend](https://img.shields.io/badge/Backend-Render-46E3B7?style=for-the-badge)](https://travelmind-backend-9ug8.onrender.com)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi)

---

## 📌 Problem Statement

Planning a trip often involves switching between multiple platforms to research tourist destinations, check weather forecasts, calculate expenses and prepare an itinerary.

This fragmented process is time-consuming and can result in poorly organized travel plans.

Traditional AI chatbots may also provide recommendations without retrieving current information from external services.

**TravelMind addresses these challenges by combining intelligent decision-making, real-world data retrieval and budget analysis in a unified travel planning platform.**

---

## 💡 Proposed Solution

TravelMind provides an intelligent travel planning assistant that:

- Generates personalized, day-wise travel itineraries.
- Retrieves tourist attractions using the OpenTripMap API.
- Fetches date-specific weather forecasts using Open-Meteo.
- Calculates estimated travel expenses and remaining budget.
- Adapts recommendations according to weather conditions.
- Uses an AI agent to dynamically select the appropriate tools.
- Presents the results through a responsive React interface.

The objective is to simplify travel planning while demonstrating the practical capabilities of **Agentic AI**.

---

## 🌐 Live Deployment

TravelMind v1.0 is deployed and accessible online.

| Component | Platform | Link |
|---|---|---|
| Frontend | Vercel | [Live TravelMind Application](https://travel-mind-beta.vercel.app) |
| Backend | Render | [FastAPI Backend](https://travelmind-backend-9ug8.onrender.com) |
| API Documentation | Swagger UI | [API Docs](https://travelmind-backend-9ug8.onrender.com/docs) |
| Source Code | GitHub | [TravelMind Repository](https://github.com/sampadabhagat15-sys/TravelMind) |

> **Note:** The backend may take some time to respond after inactivity if the hosting service has entered a sleep state.

---

## ✨ Key Features

### 🤖 1. AI-Powered Travel Planning

TravelMind generates customized itineraries based on:

- Travel destination
- Start date
- Trip duration
- Total budget
- Estimated expenses
- Personal interests

The AI organizes travel recommendations into structured, day-wise plans.

### 🧠 2. ReAct Agent Architecture

TravelMind uses a **Reasoning + Acting** approach, allowing the language model to select tools, execute actions and process external information.

The agent is not limited to generating text from its pretrained knowledge.

### 🌦️ 3. Weather-Aware Recommendations

The application retrieves weather information for the selected destination and travel dates.

The agent can recommend indoor activities during unfavorable weather and outdoor activities when conditions are suitable.

### 🏛️ 4. Real Tourist Attraction Discovery

TravelMind integrates OpenTripMap to retrieve actual tourist attractions based on the selected destination.

### 💰 5. Intelligent Budget Planning

Users can enter estimated expenses across different categories.

TravelMind calculates:

- Total estimated expenses
- Remaining budget
- Budget utilization
- Overspending alerts

The frontend also displays a visual breakdown of expenses.

### 🎨 6. Responsive User Interface

The React frontend provides:

- Modern travel-themed design
- Interactive trip planning form
- Interest selection
- Dynamic budget visualization
- Loading and error states
- Formatted AI-generated itineraries
- Visibility into the AI tools used

---

## 🧠 How TravelMind Works as a ReAct Agent

### What is ReAct?

**ReAct stands for Reasoning and Acting.**

It is an AI approach in which a language model combines reasoning with external actions.

Instead of generating an answer immediately, the agent can decide which tools are needed, execute those tools, observe their results and use the information to produce a final response.

### ReAct Workflow

```text
                  USER INPUT
                      |
                      v
              TRAVELMIND AGENT
             (Gemini + LangChain)
                      |
                      v
                 1. REASON
          Analyze travel requirements
                      |
                      v
                  2. ACT
          Select and execute tools
                      |
         +------------+------------+
         |            |            |
         v            v            v
     WEATHER       ATTRACTIONS    BUDGET
      TOOL            TOOL        TOOL
         |            |            |
         +------------+------------+
                      |
                      v
                3. OBSERVE
             Process tool outputs
                      |
                      v
             REASON AGAIN IF NEEDED
                      |
                      v
                FINAL RESPONSE
                      |
                      v
          PERSONALIZED TRAVEL PLAN
```

### Example Execution

Suppose a user requests:

> Plan a three-day trip to Mysuru with a budget of ₹10,000. I enjoy historical places and museums.

The agent performs the following process:

**Step 1 — Reasoning**

The agent identifies the information required to generate a useful travel itinerary.

**Step 2 — Tool Selection**

Based on the request, it may select:

- `find_tourist_attractions`
- `get_weather_forecast`
- `calculate_trip_budget`, when expense estimates are provided

**Step 3 — Tool Execution**

The selected tools retrieve tourist attractions, weather forecasts and budget calculations.

**Step 4 — Observation**

The agent receives and processes the tool results.

**Step 5 — Final Response**

The agent combines the information to generate a personalized itinerary containing sightseeing recommendations, weather information and budget analysis.

### Why Is This Agentic AI?

TravelMind demonstrates Agentic AI because it can:

- Interpret a user-defined objective.
- Determine which available tools are relevant.
- Execute tools through an agent framework.
- Observe external results.
- Use those observations to guide its response.
- Perform additional tool calls when required.

**The agent's tool execution sequence is dynamically determined rather than being a completely hardcoded workflow.**

---

## 🛠️ Technology Stack

| Category | Technology |
|---|---|
| Frontend | React.js |
| Frontend Language | JavaScript |
| Styling | CSS |
| Build Tool | Vite |
| Backend | Python |
| API Framework | FastAPI |
| ASGI Server | Uvicorn |
| LLM | Google Gemini |
| Agent Framework | LangChain |
| Agent Orchestration | LangGraph |
| Weather API | Open-Meteo |
| Tourist Attractions API | OpenTripMap |
| Budget Calculation | Custom Python Tool |
| Frontend Hosting | Vercel |
| Backend Hosting | Render |
| Version Control | Git & GitHub |

---

## 🔧 AI Tools

TravelMind integrates three specialized tools.

### 1. `get_weather_forecast`

**Purpose:** Retrieve weather forecasts for the selected destination and dates.

**How it works:**

1. Accepts the destination, start date and duration.
2. Converts the destination into geographical coordinates.
3. Requests forecast data from Open-Meteo.
4. Processes temperature, weather conditions and precipitation probability.
5. Returns structured weather information to the agent.

**Limitation:** The forecast is restricted to the API's supported forecast window, up to 16 days including the current day.

### 2. `find_tourist_attractions`

**Purpose:** Retrieve tourist attractions near the selected destination.

**How it works:**

1. Accepts a destination name.
2. Retrieves its geographical coordinates.
3. Queries OpenTripMap for nearby attractions.
4. Filters unnamed and duplicate results.
5. Returns structured attraction information to the agent.

The current implementation searches within approximately a 10-kilometre radius and returns up to ten attractions.

### 3. `calculate_trip_budget`

**Purpose:** Calculate estimated trip expenses and remaining budget.

**Inputs:**

- Total budget
- Transportation expenses
- Accommodation expenses
- Food expenses
- Activity expenses
- Other expenses

**Calculation:**

```text
Total Expenses =
    Transportation
  + Accommodation
  + Food
  + Activities
  + Other Expenses

Remaining Budget =
    Total Budget - Total Expenses
```

The tool determines whether the user's estimated expenses are within budget.

**Note:** Expense values are provided by the user; TravelMind does not currently retrieve live booking prices.

---

## 🏗️ System Architecture

```text
                   USER
                    |
                    v
             REACT FRONTEND
               React + Vite
                    |
                    | HTTP POST /plan
                    v
              FASTAPI BACKEND
                    |
                    v
              LANGCHAIN AGENT
                Gemini LLM
                    |
                    v
              TOOL SELECTION
                    |
         +----------+----------+
         |          |          |
         v          v          v
     Open-Meteo  OpenTripMap  Budget
      Weather    Attractions  Calculator
         |          |          |
         +----------+----------+
                    |
                    v
               TOOL RESULTS
                    |
                    v
              GEMINI REASONING
                    |
                    v
             JSON API RESPONSE
                    |
                    v
              REACT FRONTEND
                    |
                    v
          FORMATTED TRAVEL ITINERARY
```

---

## ☁️ Deployment Architecture

TravelMind uses a decoupled frontend–backend deployment architecture.

### Frontend — Vercel

The React application is deployed on Vercel.

**Live URL:** https://travel-mind-beta.vercel.app

The frontend uses the `VITE_API_BASE_URL` environment variable to communicate with the deployed backend.

### Backend — Render

The FastAPI application is deployed as a Python web service on Render.

**Backend URL:** https://travelmind-backend-9ug8.onrender.com

The backend manages:

- API requests
- Agent execution
- LLM integration
- External tool calls
- Response generation

### Environment Configuration

Sensitive API credentials are stored as backend environment variables.

```env
GOOGLE_API_KEY=your_google_api_key
OPENTRIPMAP_API_KEY=your_opentripmap_api_key
```

The production frontend is configured with:

```env
VITE_API_BASE_URL=https://travelmind-backend-9ug8.onrender.com
```

CORS is configured to allow communication between the deployed Vercel frontend and Render backend.

---

## 📂 Project Structure

```text
TravelMind/
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── agent.py
│   ├── tools.py
│   └── schemas.py
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   ├── main.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   └── assets/
│   ├── public/
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started Locally

### Prerequisites

Ensure you have installed:

- Python 3
- Node.js
- npm
- Git

You will also need:

- Google Gemini API key
- OpenTripMap API key

### Step 1 — Clone the Repository

```bash
git clone https://github.com/sampadabhagat15-sys/TravelMind.git
cd TravelMind
```

### Step 2 — Create a Python Virtual Environment

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**

```powershell
python -m venv venv
venv\Scripts\activate
```

### Step 3 — Install Backend Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Configure API Keys

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key
OPENTRIPMAP_API_KEY=your_opentripmap_api_key
```

Never commit your actual API keys to GitHub.

### Step 5 — Start the Backend

```bash
uvicorn backend.main:app --reload --port 8001
```

Backend URL:

http://127.0.0.1:8001

API documentation:

http://127.0.0.1:8001/docs

### Step 6 — Install Frontend Dependencies

Open a second terminal:

```bash
cd frontend
npm install
```

### Step 7 — Start the Frontend

```bash
npm run dev
```

Open:

http://localhost:5173

The frontend uses the local backend by default when `VITE_API_BASE_URL` is not configured.

---

## 🔌 REST API Endpoints

### `GET /`

Returns backend service information and running status.

### `POST /plan`

Generates a personalized itinerary.

**Example Request:**

```json
{
  "message": "Plan a 3-day trip to Mysuru starting on 2026-11-25. My budget is INR 10000 and I enjoy museums and historical places."
}
```

**Response Structure:**

```json
{
  "success": true,
  "response": "Generated itinerary in Markdown format",
  "tools_used": [
    "find_tourist_attractions",
    "get_weather_forecast"
  ]
}
```

The actual tools invoked depend on the user's request and the agent's decisions.

---

## 📸 Application Screenshots

The application includes:

- Landing page
- Travel planning form
- Budget visualization
- AI-generated itinerary
- Agent tool execution details

Screenshots can be added to a `screenshots/` directory and linked here.

---

## 🧪 Testing

TravelMind was tested through multiple stages.

### Individual Tool Testing

Each Python tool was tested independently to verify API responses, calculations and error handling.

### Agent Testing

The LangChain agent was tested to verify that it could select and execute the appropriate tools.

### Backend Testing

FastAPI endpoints were tested to confirm request processing and JSON response generation.

### Frontend Integration Testing

The React frontend was connected to the backend and tested using realistic travel planning inputs.

### End-to-End Testing

A complete travel planning request was tested through the user interface, including weather forecasting, attraction discovery and budget calculations.

The deployed application was also tested after configuring the production API URL and CORS settings.

---

## ⚠️ Current Limitations

TravelMind v1.0 has the following limitations:

1. Weather forecasts are limited to the supported forecast period.
2. Budget calculations use user-provided expense estimates.
3. Attraction opening hours and ticket prices are not independently verified.
4. Hotel and flight booking are not supported.
5. Interactive maps and route optimization are not yet implemented.
6. Persistent user accounts and trip history are not available.
7. Performance depends on external API availability and hosting conditions.

---

## 🔮 Future Enhancements

Planned improvements include:

- 🗺️ Interactive maps and route optimization
- 🏨 Hotel and flight booking integrations
- 💳 Real-time travel pricing
- 📄 Downloadable PDF itineraries
- 👤 User authentication and saved trips
- 🌍 Multi-destination travel planning
- 🤖 Advanced agent memory and personalization
- 📱 Improved mobile experience

---

## 🎯 Project Objectives

TravelMind was developed to:

- Explore practical applications of Agentic AI.
- Understand ReAct-style reasoning and tool execution.
- Integrate LLMs with real-world APIs.
- Develop a complete full-stack AI application.
- Implement REST API communication.
- Deploy a working AI-powered application to cloud hosting platforms.

---

## 👩‍💻 Developer

**Sampada Bhagat**

B.Tech — Computer Science & Engineering

Dayananda Sagar University, Bengaluru

**GitHub:** [@sampadabhagat15-sys](https://github.com/sampadabhagat15-sys)

**Project Repository:** [TravelMind](https://github.com/sampadabhagat15-sys/TravelMind)

**Live Application:** [Launch TravelMind](https://travel-mind-beta.vercel.app)

---

### ⭐ Support the Project

If you find TravelMind useful or interesting, consider starring the repository!

**TravelMind demonstrates how Agentic AI, real-world API integration and modern full-stack development can work together to build an intelligent travel planning experience.**
