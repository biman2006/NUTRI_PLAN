import { useState } from "react";

function App() {
  const [age, setAge] = useState("");
  const [height, setHeight] = useState("");
  const [weight, setWeight] = useState("");
  const [goal, setGoal] = useState("cut");

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/diet-plan", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          age: Number(age),
          height: Number(height),
          weight: Number(weight),
          goal: goal,
        }),
      });

      if (!response.ok) {
        throw new Error("API Error! Check backend running or input invalid.");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: "30px", fontFamily: "Arial" }}>
      <h1>🥗 Diet Planner Website</h1>
      <p>Enter your details and generate your diet plan.</p>

      <form
        onSubmit={handleSubmit}
        style={{
          display: "flex",
          flexDirection: "column",
          gap: "12px",
          maxWidth: "400px",
        }}
      >
        <input
          type="number"
          placeholder="Enter Age"
          value={age}
          onChange={(e) => setAge(e.target.value)}
          required
        />

        <input
          type="number"
          step="0.01"
          placeholder="Enter Height (meter)"
          value={height}
          onChange={(e) => setHeight(e.target.value)}
          required
        />

        <input
          type="number"
          step="0.01"
          placeholder="Enter Weight (kg)"
          value={weight}
          onChange={(e) => setWeight(e.target.value)}
          required
        />

        <select value={goal} onChange={(e) => setGoal(e.target.value)}>
          <option value="cut">Cut</option>
          <option value="bulk">Bulk</option>
          <option value="maintain">Maintain</option>
        </select>

        <button type="submit" disabled={loading}>
          {loading ? "Generating..." : "Generate Diet Plan"}
        </button>
      </form>

      {error && (
        <p style={{ color: "red", marginTop: "20px" }}>❌ Error: {error}</p>
      )}

      {result && (
        <div style={{ marginTop: "20px" }}>
          <h2>✅ Diet Plan Result</h2>
          <pre
            style={{
              background: "#111",
              color: "lime",
              padding: "15px",
              borderRadius: "10px",
              overflowX: "auto",
            }}
          >
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}

export default App;
