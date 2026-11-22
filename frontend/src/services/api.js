
const API_BASE_URL = "http://127.0.0.1:8001";

export async function generateItinerary(message) {
  const response = await fetch(`${API_BASE_URL}/plan`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message: message,
    }),
  });

  if (!response.ok) {
    let errorMessage = "Failed to generate itinerary.";

    try {
      const errorData = await response.json();
      errorMessage = errorData.detail || errorMessage;
    } catch {
      // Use the default error message.
    }

    throw new Error(errorMessage);
  }

  return await response.json();
}
