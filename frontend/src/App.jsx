import { useState } from 'react';
import './App.css';

function App() {
  // Form state - all 6 required fields
  const [formData, setFormData] = useState({
    age: '',
    gender: '',
    height: '',
    weight: '',
    activity_level: '',
    goal: ''
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';
      const response = await fetch(`${apiUrl}/diet-plan`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          age: Number(formData.age),
          gender: formData.gender,
          height: Number(formData.height),
          weight: Number(formData.weight),
          activity_level: formData.activity_level,
          goal: formData.goal
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to generate plan');
      }

      const data = await response.json();
      setResult(data.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const activityLevels = [
    { value: 'sedentary', label: 'Sedentary', desc: 'Little or no exercise' },
    { value: 'lightly_active', label: 'Light', desc: '1-3 days/week' },
    { value: 'moderately_active', label: 'Moderate', desc: '3-5 days/week' },
    { value: 'very_active', label: 'Very Active', desc: '6-7 days/week' },
    { value: 'extra_active', label: 'Athlete', desc: 'Intense daily training' }
  ];

  const goals = [
    { value: 'cut', label: 'Cut', emoji: '📉', desc: 'Lose weight' },
    { value: 'maintain', label: 'Maintain', emoji: '⚖️', desc: 'Stay balanced' },
    { value: 'bulk', label: 'Bulk', emoji: '💪', desc: 'Build muscle' }
  ];

  return (
    <div className="app">
      {/* Hero Section */}
      <header className="hero">
        <div className="hero-accent"></div>
        <img src="/NutiPlanLogo.png" alt="Nutri Plan Logo" className="hero-logo" />
        <h1 className="hero-title">
          Your Body,<br />
          <span className="hero-emphasis">Your Science</span>
        </h1>
        <p className="hero-subtitle">
          Nutrition planning built on metabolic science,<br />designed for living humans.
        </p>
      </header>

      {/* Main Container */}
      <main className="container">
        {!result ? (
          <form className="diet-form" onSubmit={handleSubmit}>
            {/* Personal Info Section */}
            <section className="form-section">
              <h2 className="section-title">Your Vitals</h2>

              <div className="input-grid">
                <div className="input-group">
                  <label htmlFor="age">Age</label>
                  <input
                    id="age"
                    type="number"
                    min="9"
                    max="119"
                    value={formData.age}
                    onChange={(e) => handleChange('age', e.target.value)}
                    placeholder="25"
                    required
                  />
                </div>

                <div className="input-group">
                  <label htmlFor="height">Height (meters)</label>
                  <input
                    id="height"
                    type="number"
                    step="0.01"
                    min="0.5"
                    max="3"
                    value={formData.height}
                    onChange={(e) => handleChange('height', e.target.value)}
                    placeholder="1.75"
                    required
                  />
                </div>

                <div className="input-group">
                  <label htmlFor="weight">Weight (kg)</label>
                  <input
                    id="weight"
                    type="number"
                    step="0.1"
                    min="26"
                    max="299"
                    value={formData.weight}
                    onChange={(e) => handleChange('weight', e.target.value)}
                    placeholder="70"
                    required
                  />
                </div>
              </div>

              {/* Gender Selection */}
              <div className="gender-selector">
                <label className="selector-label">Gender</label>
                <div className="gender-options">
                  <button
                    type="button"
                    className={`gender-btn ${formData.gender === 'male' ? 'active' : ''}`}
                    onClick={() => handleChange('gender', 'male')}
                  >
                    <span className="gender-icon">♂</span>
                    <span>Male</span>
                  </button>
                  <button
                    type="button"
                    className={`gender-btn ${formData.gender === 'female' ? 'active' : ''}`}
                    onClick={() => handleChange('gender', 'female')}
                  >
                    <span className="gender-icon">♀</span>
                    <span>Female</span>
                  </button>
                </div>
              </div>
            </section>

            {/* Activity Level Section */}
            <section className="form-section">
              <h2 className="section-title">Activity Level</h2>
              <div className="activity-grid">
                {activityLevels.map((level) => (
                  <button
                    key={level.value}
                    type="button"
                    className={`activity-card ${formData.activity_level === level.value ? 'active' : ''}`}
                    onClick={() => handleChange('activity_level', level.value)}
                  >
                    <span className="activity-label">{level.label}</span>
                    <span className="activity-desc">{level.desc}</span>
                  </button>
                ))}
              </div>
            </section>

            {/* Goal Section */}
            <section className="form-section">
              <h2 className="section-title">Your Goal</h2>
              <div className="goal-grid">
                {goals.map((goal) => (
                  <button
                    key={goal.value}
                    type="button"
                    className={`goal-card ${formData.goal === goal.value ? 'active' : ''}`}
                    onClick={() => handleChange('goal', goal.value)}
                  >
                    <span className="goal-emoji">{goal.emoji}</span>
                    <span className="goal-label">{goal.label}</span>
                    <span className="goal-desc">{goal.desc}</span>
                  </button>
                ))}
              </div>
            </section>

            {/* Submit Button */}
            <button
              type="submit"
              className="submit-btn"
              disabled={loading || !formData.gender || !formData.activity_level || !formData.goal}
            >
              {loading ? (
                <span className="btn-loading">Analyzing...</span>
              ) : (
                <span>Generate My Plan</span>
              )}
            </button>

            {error && (
              <div className="error-message">
                <strong>Error:</strong> {error}
              </div>
            )}
          </form>
        ) : (
          <div className="results">
            {/* Stats Overview */}
            <div className="results-header">
              <h2 className="results-title">Your Nutritional Blueprint</h2>
              <button className="reset-btn" onClick={() => setResult(null)}>
                Start Over
              </button>
            </div>

            {/* Key Metrics */}
            <div className="metrics-grid">
              <div className="metric-card">
                <span className="metric-label">BMI</span>
                <span className="metric-value">{result.bmi.value}</span>
                <span className="metric-category">{result.bmi.category}</span>
              </div>

              <div className="metric-card">
                <span className="metric-label">BMR</span>
                <span className="metric-value">{result.metabolism.bmr}</span>
                <span className="metric-unit">kcal/day at rest</span>
              </div>

              <div className="metric-card">
                <span className="metric-label">TDEE</span>
                <span className="metric-value">{result.metabolism.tdee}</span>
                <span className="metric-unit">total daily</span>
              </div>

              <div className="metric-card highlight">
                <span className="metric-label">Target Calories</span>
                <span className="metric-value large">{result.macros.calories}</span>
                <span className="metric-unit">kcal/day</span>
              </div>

              <div className="metric-card highlight">
                <span className="metric-label">Protein Goal</span>
                <span className="metric-value large">{result.macros.protein}g</span>
                <span className="metric-unit">daily intake</span>
              </div>
            </div>

            {/* Meal Plan */}
            <div className="meal-plan">
              <h3 className="plan-title">Your Daily Meal Plan</h3>
              <div className="meal-grid">
                {Object.entries(result.diet_chart).map(([meal, foods]) => (
                  <div key={meal} className="meal-card">
                    <h4 className="meal-name">{meal.charAt(0).toUpperCase() + meal.slice(1)}</h4>
                    <ul className="meal-list">
                      {foods.map((food, idx) => (
                        <li key={idx}>{food}</li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
