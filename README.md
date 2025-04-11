# Weather App

A full-stack weather application built with Django and React that provides real-time weather information and forecasts.

## Features

- Real-time weather data for any city
- 24-hour weather forecast
- Beautiful and responsive UI
- Search history tracking
- Detailed weather information including:
  - Temperature
  - Humidity
  - Wind speed
  - Weather description
  - Weather icons

## Tech Stack

### Backend
- Django
- Django REST Framework
- SQLite
- OpenWeatherMap API

### Frontend
- React
- CSS3
- OpenWeatherMap Icons

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/weather-app.git
cd weather-app
```

2. Install backend dependencies:
```bash
pip install -r requirements.txt
```

3. Install frontend dependencies:
```bash
cd frontend
npm install
```

4. Create a `.env` file in the root directory:
```bash
DEBUG=True
SECRET_KEY=your-secret-key
OPENWEATHER_API_KEY=your-api-key
```

5. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Start the backend server:
```bash
python manage.py runserver
```

7. Start the frontend development server:
```bash
cd frontend
npm start
```

## Usage

1. Open your browser and go to `http://localhost:3001`
2. Enter a city name in the search box
3. Click "Get Weather" to see current weather and forecast

## API Endpoints

- `GET /api/cities/` - List all cities
- `GET /api/cities/search/?city={city_name}` - Search weather by city
- `GET /api/weather/` - List all weather data
- `GET /api/searches/` - List search history

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenWeatherMap for providing the weather data API
- Django and React communities for their amazing frameworks 
