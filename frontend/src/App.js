import React, { useState } from 'react';
import './App.css';

const WeatherApp = () => {
  const [city, setCity] = useState("");
  const [weatherData, setWeatherData] = useState(null);
  const [forecastData, setForecastData] = useState([]);
  const [error, setError] = useState("");

  const handleInputChange = (e) => {
    setCity(e.target.value);
  };

  const fetchWeather = async () => {
    if (!city) {
      setError("Please enter a city!");
      setWeatherData(null);
      setForecastData([]);
      return;
    }

    try {
      // Fetch current weather using the new endpoint
      const response = await fetch(`http://localhost:8000/api/cities/search/?city=${city}`);
      const data = await response.json();

      if (response.status !== 200) {
        setError(data.error || "Something went wrong. Please try again.");
        setWeatherData(null);
        setForecastData([]);
        return;
      }

      // Transform the response to match the expected format
      setWeatherData({
        city: data.city.name,
        temperature: data.weather.temperature,
        description: data.weather.description,
        humidity: data.weather.humidity,
        wind_speed: data.weather.wind_speed,
        icon: data.weather.icon || '01d' // Default icon if not provided
      });

      // Set forecast data
      setForecastData(data.forecast || []);
      setError("");

    } catch (err) {
      setError("Something went wrong. Please try again.");
      setWeatherData(null);
      setForecastData([]);
    }
  };

  return (
    <div className="weather-container">
      <h1 className="title">Weather App</h1>

      <div className="input-box">
        <input
          type="text"
          className="input-field"
          placeholder="Enter city"
          value={city}
          onChange={handleInputChange}
        />
        <button onClick={fetchWeather} className="button">Get Weather</button>
      </div>

      {error && <div className="error">{error}</div>}

      {weatherData && (
        <div className="weather-info">
          <h2>{weatherData.city}</h2>
          <img
            src={`https://openweathermap.org/img/wn/${weatherData.icon}@4x.png`}
            alt="weather icon"
            className="weather-icon-large"
          />
          <p className="temp-big">{weatherData.temperature}°C</p>
          <p>Description: {weatherData.description}</p>
          <p>Humidity: {weatherData.humidity}%</p>
          <p>Wind Speed: {weatherData.wind_speed} m/s</p>
        </div>
      )}

      {forecastData.length > 0 && (
        <div className="forecast-container">
          <h3>24-Hour Forecast</h3>
          <div className="forecast-grid">
            {forecastData.map((item, index) => (
              <div key={index} className="forecast-card">
                <p className="forecast-time">{new Date(item.dt_txt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</p>
                <img
                  src={`https://openweathermap.org/img/wn/${item.icon}@2x.png`}
                  alt="weather icon"
                  className="weather-icon"
                />
                <p className="forecast-desc">{item.description}</p>
                <p className="forecast-temp">{item.temp}°C</p>
                <p className="forecast-details">
                  H: {item.humidity}% | W: {item.wind_speed} m/s
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default WeatherApp;
