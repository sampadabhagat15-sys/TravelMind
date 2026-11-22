
import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { generateItinerary } from "./services/api";
import "./App.css";

const expenseCategories = [
  { key: "transportation", label: "Transportation", color: "#126782", icon: "🚗" },
  { key: "accommodation", label: "Accommodation", color: "#34a0a4", icon: "🏨" },
  { key: "food", label: "Food & Dining", color: "#76c893", icon: "🍽️" },
  { key: "activities", label: "Activities", color: "#e9b44c", icon: "🎟️" },
  { key: "other", label: "Other Expenses", color: "#9b8bc0", icon: "🛍️" },
];

const toolNames = {
  calculate_trip_budget: "Budget Calculator",
  get_weather_forecast: "Live Weather Forecast",
  find_tourist_attractions: "Tourist Attraction Finder",
};

function App() {
  const [destination, setDestination] = useState("");
  const [travelDate, setTravelDate] = useState("");
  const [duration, setDuration] = useState(2);
  const [budget, setBudget] = useState("");
  const [interests, setInterests] = useState("");
  const [showExpenses, setShowExpenses] = useState(false);

  const [expenses, setExpenses] = useState({
    transportation: "",
    accommodation: "",
    food: "",
    activities: "",
    other: "",
  });

  const [itinerary, setItinerary] = useState("");
  const [toolsUsed, setToolsUsed] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const now = new Date();

  const today = [
    now.getFullYear(),
    String(now.getMonth() + 1).padStart(2, "0"),
    String(now.getDate()).padStart(2, "0"),
  ].join("-");

  const totalExpenses = Object.values(expenses).reduce(
    (total, value) => total + (Number(value) || 0),
    0
  );

  const remainingBudget = Number(budget) - totalExpenses;
  const hasBudget = budget !== "";
  const withinBudget = remainingBudget >= 0;

  const expensesComplete = expenseCategories
    .filter((category) => category.key !== "other")
    .every((category) => expenses[category.key] !== "");

  const formatCurrency = (amount) =>
    new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
      maximumFractionDigits: 2,
    }).format(amount);

  const handleExpenseChange = (category, value) => {
    setExpenses((previous) => ({
      ...previous,
      [category]: value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    setLoading(true);
    setError("");
    setItinerary("");
    setToolsUsed([]);

    const budgetDetails = hasBudget
      ? `My total travel budget is INR ${budget}.`
      : "I have not specified a total travel budget.";

    const expenseDetails = showExpenses && hasBudget
      ? `
        My estimated expenses in INR for the entire trip:

        Transportation: ${Number(expenses.transportation) || 0}
        Accommodation: ${Number(expenses.accommodation) || 0}
        Food: ${Number(expenses.food) || 0}
        Activities: ${Number(expenses.activities) || 0}
        Other expenses: ${Number(expenses.other) || 0}

        Use calculate_trip_budget to calculate my total
        expenses and remaining budget.

        If the budget is exceeded, suggest practical
        ways to reduce expenses.

        These are user-provided estimates, not verified
        market prices.
      `
      : `
        Individual expense estimates have not been
        provided with a total budget. Do not assume
        that the trip is affordable.
      `;

    const message = `
      Plan a ${duration}-day trip to ${destination}.

      Travel start date: ${travelDate}.
      Today's date: ${today}.

      My interests:
      ${interests.trim() || "General sightseeing"}.

      ${budgetDetails}
      ${expenseDetails}

      Use the tourist attraction finder to retrieve
      real tourist attractions.

      Use the weather forecast tool to retrieve
      forecasts for my travel dates.

      Create a personalized, weather-aware itinerary.

      Include calendar dates, daily weather conditions,
      and morning, afternoon and evening activities.

      Include a detailed budget analysis when expense
      estimates are provided.

      Do not invent weather forecasts, opening hours,
      travel times, ticket prices, or expense estimates.

      Use clean Markdown formatting.
    `;

    try {
      const data = await generateItinerary(message);

      if (!data.success) {
        throw new Error("The itinerary could not be generated.");
      }

      setItinerary(data.response);
      setToolsUsed(data.tools_used || []);

    } catch (err) {
      setError(err.message || "Something went wrong. Please try again.");

    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">

      {/* NAVIGATION */}

      <nav className="navbar">
        <a className="brand" href="#">
          <span className="brand-icon">✈</span>
          Travel<span>Mind</span>
        </a>

        <div className="nav-links">
          <a href="#features">Features</a>
          <a href="#planner">Plan a Trip</a>
        </div>

        <span className="ai-badge">
          <span className="status-dot" />
          AI Powered
        </span>
      </nav>

      {/* HERO SECTION */}

      <section className="hero">
        <div className="hero-decoration">✈</div>

        <div className="hero-content">
          <span className="hero-tag">
            YOUR SMART TRAVEL COMPANION
          </span>

          <h1>
            Explore more.
            <br />
            <span>Plan smarter.</span>
          </h1>

          <p>
            Discover extraordinary destinations with
            personalized itineraries, date-specific weather
            forecasts and intelligent budget planning.
          </p>

          <a href="#planner" className="hero-button">
            Start Planning <span>↗</span>
          </a>
        </div>

        <div className="hero-visual">
          <div className="orbit orbit-one" />
          <div className="orbit orbit-two" />
          <div className="hero-globe">🌍</div>
          <div className="floating-tag tag-one">☀ Weather aware</div>
          <div className="floating-tag tag-two">📍 Real destinations</div>
          <div className="floating-tag tag-three">₹ Budget smart</div>
        </div>
      </section>

      {/* FEATURES */}

      <section className="feature-grid" id="features">

        {[
          ["✦", "AI-Powered Planning",
            "Personalized itineraries built around your interests."],
          ["☀", "Weather Intelligence",
            "Date-specific forecasts for smarter travel decisions."],
          ["⌖", "Real Attractions",
            "Discover places using real-world geographic data."],
          ["₹", "Smart Budgeting",
            "Track estimated expenses and avoid overspending."],
        ].map(([icon, title, description]) => (
          <div className="feature-card" key={title}>
            <div className="feature-icon">{icon}</div>
            <h3>{title}</h3>
            <p>{description}</p>
          </div>
        ))}

      </section>

      {/* PLANNER HEADING */}

      <div className="section-heading" id="planner">
        <span className="eyebrow">DESIGN YOUR JOURNEY</span>
        <h2>Your adventure starts here.</h2>
        <p>
          Set your preferences and let TravelMind handle the planning.
        </p>
      </div>

      {/* MAIN WORKSPACE */}

      <main className="workspace">

        <section className="planner-card">

          <div className="card-heading">
            <div className="feature-icon">✈</div>
            <div>
              <h2>Trip Preferences</h2>
              <p>Tell us about your next adventure.</p>
            </div>
          </div>

          <form onSubmit={handleSubmit}>

            <label htmlFor="destination">Destination</label>
            <input
              id="destination"
              type="text"
              placeholder="Where do you want to go?"
              value={destination}
              onChange={(e) => setDestination(e.target.value)}
              required
            />

            <div className="form-row">
              <div className="form-field">
                <label htmlFor="travelDate">Start Date</label>
                <input
                  id="travelDate"
                  type="date"
                  min={today}
                  value={travelDate}
                  onChange={(e) => setTravelDate(e.target.value)}
                  required
                />
              </div>

              <div className="form-field">
                <label htmlFor="duration">Duration (Days)</label>
                <input
                  id="duration"
                  type="number"
                  min="1"
                  max="30"
                  value={duration}
                  onChange={(e) => setDuration(e.target.value)}
                  required
                />
              </div>
            </div>

            <label htmlFor="budget">Total Budget (₹)</label>
            <input
              id="budget"
              type="number"
              min="0"
              step="0.01"
              placeholder="e.g. 10000"
              value={budget}
              onChange={(e) => setBudget(e.target.value)}
              required={showExpenses}
            />

            <label className="budget-toggle">
              <input
                type="checkbox"
                checked={showExpenses}
                onChange={(e) => setShowExpenses(e.target.checked)}
              />
              Add estimated trip expenses
            </label>

            {/* BUDGET PLANNER */}

            {showExpenses && (
              <div className="budget-planner">
                <h3>Trip Budget Breakdown</h3>
                <p className="budget-description">
                  Estimated expenses for the entire trip.
                  Enter 0 where not applicable.
                </p>

                <div className="expense-grid">
                  {expenseCategories.map((category) => (
                    <div className="expense-field" key={category.key}>
                      <label htmlFor={category.key}>
                        {category.icon} {category.label}
                      </label>

                      <input
                        id={category.key}
                        type="number"
                        min="0"
                        step="0.01"
                        placeholder="₹ 0"
                        value={expenses[category.key]}
                        onChange={(e) =>
                          handleExpenseChange(category.key, e.target.value)
                        }
                        required={category.key !== "other"}
                      />
                    </div>
                  ))}
                </div>

                <div className="budget-summary">
                  <div className="budget-stat">
                    <span>Total Expenses</span>
                    <strong>{formatCurrency(totalExpenses)}</strong>
                  </div>

                  {hasBudget && (
                    <div className="budget-stat">
                      <span>Remaining Budget</span>
                      <strong style={{
                        color: withinBudget ? "#16835d" : "#d14343"
                      }}>
                        {formatCurrency(remainingBudget)}
                      </strong>
                    </div>
                  )}
                </div>

                {totalExpenses > 0 && (
                  <>
                    <div className="expense-bar">
                      {expenseCategories.map((category) => (
                        <div
                          key={category.key}
                          title={category.label}
                          style={{
                            backgroundColor: category.color,
                            width: `${
                              (Number(expenses[category.key]) || 0)
                              / Math.max(Number(budget) || 0, totalExpenses, 1)
                              * 100
                            }%`,
                          }}
                        />
                      ))}
                    </div>

                    <div className="expense-legend">
                      {expenseCategories.map((category) => (
                        <span key={category.key}>
                          <span
                            className="legend-dot"
                            style={{ backgroundColor: category.color }}
                          />
                          {category.label}
                        </span>
                      ))}
                    </div>
                  </>
                )}

                {hasBudget && expensesComplete && (
                  <div className={`budget-status ${
                    withinBudget ? "budget-success" : "budget-warning"
                  }`}>
                    {withinBudget
                      ? "✓ Estimated expenses are within budget."
                      : `⚠ Budget exceeded by ${formatCurrency(
                          Math.abs(remainingBudget)
                        )}.`}
                  </div>
                )}
              </div>
            )}

            <label htmlFor="interests">Travel Interests</label>
            <textarea
              id="interests"
              placeholder="History, nature, food, adventure..."
              value={interests}
              onChange={(e) => setInterests(e.target.value)}
              rows="3"
            />

            <div className="interest-chips">
              {["History", "Nature", "Food", "Adventure", "Museums", "Shopping"]
                .map((interest) => (
                  <button
                    key={interest}
                    type="button"
                    className="interest-chip"
                    onClick={() =>
                      setInterests((previous) => {
                        const items = previous.split(",")
                          .map((item) => item.trim())
                          .filter(Boolean);

                        if (items.some(
                          (item) => item.toLowerCase() === interest.toLowerCase()
                        )) return previous;

                        return [...items, interest].join(", ");
                      })
                    }
                  >
                    + {interest}
                  </button>
                ))}
            </div>

            <button
              className="generate-button"
              type="submit"
              disabled={loading}
            >
              {loading ? "Creating your adventure..." : "✦ Generate My Itinerary"}
            </button>

            <p className="form-note">
              Powered by Gemini AI and real-world data sources.
            </p>

          </form>
        </section>

        {/* RESULTS PANEL */}

        <section className="results-card">

          <div className="card-heading">
            <div className="feature-icon">⌖</div>
            <div>
              <h2>Your Travel Itinerary</h2>
              <p>A journey designed just for you.</p>
            </div>
          </div>

          {!itinerary && !loading && !error && (
            <div className="empty-state">
              <div className="empty-illustration">🗺️</div>
              <h2>Every journey begins with a plan.</h2>
              <p>
                Fill in your trip preferences and generate
                a personalized AI travel itinerary.
              </p>

              <div className="empty-tags">
                <span>✦ Personalized</span>
                <span>☀ Weather aware</span>
                <span>₹ Budget smart</span>
              </div>
            </div>
          )}

          {loading && (
            <div className="loading-state" role="status">
              <div className="spinner" />
              <h3>Crafting your perfect journey...</h3>
              <p>
                Our AI agent is retrieving travel data,
                checking relevant tools and organizing your itinerary.
              </p>
              <div className="loading-track">
                <div />
              </div>
            </div>
          )}

          {error && (
            <div className="error-message" role="alert">
              <strong>Unable to generate itinerary</strong>
              <p>{error}</p>
              <p>Please try again.</p>
            </div>
          )}

          {itinerary && (
            <section className="itinerary-result">

              <div className="result-badge">
                ✓ Your personalized itinerary is ready
              </div>

              <div className="markdown-content">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {itinerary}
                </ReactMarkdown>
              </div>

              {toolsUsed.length > 0 && (
                <div className="tools-section">
                  <span className="eyebrow">AGENT EXECUTION</span>
                  <h3>AI Tools Used</h3>
                  <p>
                    Real-world tools called by the TravelMind ReAct agent.
                  </p>

                  <div className="tool-list">
                    {[...new Set(toolsUsed)].map((tool) => (
                      <div className="tool-item" key={tool}>
                        <span className="tool-check">✓</span>
                        <div>
                          <strong>{toolNames[tool] || tool}</strong>
                          <small>{tool}</small>
                        </div>
                        <span className="tool-status">Called</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

            </section>
          )}

        </section>
      </main>

      {/* FOOTER */}

      <footer>
        <div className="footer-brand">✈ TravelMind</div>
        <p>Intelligent Travel Planning · Powered by Agentic AI</p>
        <span>
          Gemini AI · LangChain · FastAPI · React
        </span>
        <p className="copyright">© 2026 TravelMind</p>
      </footer>

    </div>
  );
}

export default App;






