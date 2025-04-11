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
      // Fetch current weather
      const weatherRes = await fetch(`http://localhost:8000/api/get-weather/?city=${city}`);
      const weatherJson = await weatherRes.json();

      if (weatherJson.error) {
        setError(weatherJson.error);
        setWeatherData(null);
        setForecastData([]);
        return;
      } else {
        setWeatherData(weatherJson);
        setError("");
      }

      // Fetch forecast
      const forecastRes = await fetch(`http://localhost:8000/api/get-forecast/?city=${city}`);
      const forecastJson = await forecastRes.json();

      setForecastData(forecastJson.forecast);

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
          <h3>Next Forecast (5-Day)</h3>
          <div className="forecast-grid">
            {forecastData.map((item, index) => (
              <div key={index} className="forecast-card">
                <p className="forecast-time">{item.dt_txt}</p>
                <img
                  src={`https://openweathermap.org/img/wn/${item.weather[0].icon}@2x.png`}
                  alt="icon"
                  className="weather-icon"
                />
                <p className="forecast-desc">{item.weather[0].description}</p>
                <p className="forecast-temp">{item.main.temp}°C</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default WeatherApp;
