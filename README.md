# Professor Finder 🎓

A Django web application that helps find professors by location, institution, and expertise using AI-powered search with Tavily and Groq APIs.

## Features

- **Manual Input Forms**: Type in any country, city, university, department, and skills directly
- **Autocomplete Suggestions**: HTML5 datalist provides suggestions from existing database entries
- **Skills-Based Search**: Filter professors by specific expertise areas (AI, ML, Data Science, etc.)
- **AI-Powered Results**: Uses Tavily for web search and Groq LLM for data extraction
- **Professional Results Display**: Clean cards with contact info and skill tags
- **Export Functionality**: Download results as CSV
- **Responsive Design**: Bootstrap-based UI that works on all devices

## Technology Stack

- **Backend**: Django 5.2.5 (Python)
- **Frontend**: HTML, CSS (Bootstrap 5), JavaScript
- **Search API**: Tavily Search API
- **LLM Processing**: Groq LLaMA 3
- **Database**: SQLite (default)

## Setup Instructions

### 1. Prerequisites
- Python 3.8+ installed
- Git installed

### 2. Clone and Setup
```bash
git clone <repository-url>
cd professor-finder
```

### 3. Create Virtual Environment
```bash
python -m venv .venv

# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install django requests python-dotenv
```

### 5. Configure API Keys
Create a `.env` file in the project root:
```env
# API Configuration - Get these keys from respective providers
TAVILY_API_KEY=your_tavily_api_key_here
GROQ_API_KEY=your_groq_api_key_here

# Django Configuration
SECRET_KEY=your_secret_key_here
DEBUG=True
```

**Get API Keys:**
- **Tavily API**: Visit [tavily.com](https://tavily.com) → Sign up → Get API key (free tier available)
- **Groq API**: Visit [groq.com](https://groq.com) → Sign up → Get API key (free tier available)

### 6. Setup Database
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py load_sample_data  # Load test universities
```

### 7. Create Admin User (Optional)
```bash
python manage.py createsuperuser
```

### 8. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to use the application.

## API Endpoints

### REST API Endpoints

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/api/search/` | POST | Search for professors | JSON body: `{"country": "USA", "city": "Cambridge", "university": "MIT", "department": "CS", "skills": "AI"}` |
| `/api/professors/` | GET | List all professors with filtering | Query params: `country`, `city`, `university`, `department`, `skills`, `page`, `page_size` |
| `/api/countries/` | GET | List all countries | None |
| `/api/cities/<country_id>/` | GET | List cities by country | `country_id` in URL |
| `/api/universities/<city_id>/` | GET | List universities by city | `city_id` in URL |
| `/api/departments/<university_id>/` | GET | List departments by university | `university_id` in URL |
| `/admin/` | GET/POST | Django admin interface | Admin credentials required |

### Example Usage

#### Search for Professors (POST)
```bash
curl -X POST http://127.0.0.1:8000/api/search/ \
  -H "Content-Type: application/json" \
  -d '{
    "country": "United States",
    "city": "Cambridge", 
    "university": "MIT",
    "department": "Computer Science",
    "skills": "artificial intelligence"
  }'
```

**Response:**
```json
{
  "success": true,
  "results_found": 5,
  "professors": [
    {
      "id": 1,
      "name": "Dr. John Smith",
      "email": "jsmith@mit.edu",
      "portfolio_link": "https://www.mit.edu/~jsmith",
      "skills": "artificial intelligence, machine learning",
      "department": "Computer Science",
      "university": "MIT",
      "city": "Cambridge",
      "country": "United States",
      "created": true
    }
  ]
}
```

#### List Professors with Filtering (GET)
```bash
curl "http://127.0.0.1:8000/api/professors/?university=MIT&skills=AI&page=1&page_size=10"
```

**Response:**
```json
{
  "success": true,
  "total_count": 25,
  "page": 1,
  "page_size": 10,
  "professors": [...]
}
```

#### Get Countries (GET)
```bash
curl http://127.0.0.1:8000/api/countries/
```

**Response:**
```json
{
  "success": true,
  "countries": [
    {"id": 1, "name": "United States", "code": "USA"},
    {"id": 2, "name": "United Kingdom", "code": "GBR"}
  ]
}
```

#### Get Cities by Country (GET)
```bash
curl http://127.0.0.1:8000/api/cities/1/
```

**Response:**
```json
{
  "success": true,
  "cities": [
    {"id": 1, "name": "Cambridge"},
    {"id": 2, "name": "Boston"}
  ]
}
```

## Usage

### API Usage Process
1. **Get Countries**: Call `/api/countries/` to get available countries
2. **Get Cities**: Call `/api/cities/<country_id>/` to get cities for selected country
3. **Get Universities**: Call `/api/universities/<city_id>/` to get universities for selected city
4. **Get Departments**: Call `/api/departments/<university_id>/` to get departments for selected university
5. **Search Professors**: Call `/api/search/` with JSON payload to find professors
6. **List Results**: Call `/api/professors/` to get paginated results with filtering

### Search Query Construction
The system builds queries like:
```
"professors AI Machine Learning Computer Science MIT Cambridge United States email portfolio site:.edu OR site:.ac"
```

### API Workflow
1. **Tavily Search**: Finds academic web pages matching criteria
2. **Groq LLM**: Extracts structured professor data from search results
3. **Database Storage**: Saves results for retrieval via API

## Project Structure

```
professor_finder/
├── manage.py
├── .env                          # API keys and config
├── professor_finder/            # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── search/                      # Main search app
    ├── models.py               # Database models
    ├── forms.py                # Search forms
    ├── views.py                # Request handlers
    ├── services.py             # API integrations
    ├── urls.py                 # URL routing
    ├── admin.py                # Admin interface
    ├── templates/              # HTML templates
    │   └── search/
    │       └── home.html
    └── management/             # Custom commands
        └── commands/
            └── load_sample_data.py
```

## External API Integration

### Tavily Search API
- **Endpoint**: `https://api.tavily.com/search`
- **Purpose**: Web search for academic profiles
- **Authentication**: API key in request body
- **Query Format**: Constructs targeted academic search strings
- **Response**: Returns relevant web page content and URLs
- **Rate Limits**: Check Tavily documentation for current limits

#### Example Tavily Request
```json
{
  "api_key": "your_tavily_api_key",
  "query": "professors artificial intelligence Computer Science MIT Cambridge United States email portfolio site:.edu OR site:.ac",
  "search_depth": "advanced",
  "include_answer": false,
  "include_images": false,
  "include_raw_content": true,
  "max_results": 10
}
```

### Groq LLM API
- **Endpoint**: `https://api.groq.com/openai/v1/chat/completions`
- **Purpose**: Extract structured data from search results
- **Model**: LLaMA 3-8B (free tier compatible)
- **Authentication**: Bearer token in Authorization header
- **Input**: Combined search result text
- **Output**: JSON array of professor objects

#### Example Groq Request
```json
{
  "model": "llama3-8b-8192",
  "messages": [
    {
      "role": "system", 
      "content": "You are a precise data extraction assistant. Return only valid JSON arrays with the exact structure requested."
    },
    {
      "role": "user",
      "content": "Extract professor information from search results..."
    }
  ],
  "temperature": 0.1,
  "max_tokens": 2000
}
```

## Internal API Flow

### Search Workflow
1. **Form Validation**: Django validates user input
2. **Tavily Search**: Query construction and web search
3. **Data Processing**: Groq LLM extracts structured data
4. **Database Storage**: Save professors and institutional hierarchy
5. **Response**: Display results with pagination

### Data Models Hierarchy
```
Country → City → University → Department → Professor
```

## API Integration Details

### Tavily Search API
- **Purpose**: Web search for academic profiles
- **Query**: Constructs targeted academic search strings
- **Response**: Returns relevant web page content and URLs

### Groq LLM API
- **Purpose**: Extract structured data from search results
- **Model**: LLaMA 3-8B (free tier)
- **Input**: Combined search result text
- **Output**: JSON array of professor objects

## Database Models

- **Country**: Countries with ISO codes
- **City**: Cities linked to countries
- **University**: Universities in specific cities
- **Department**: Departments within universities
- **Professor**: Professor profiles with skills and contact info

## Admin Interface

Access at `/admin/` to:
- Manage location data (countries, cities, universities, departments)
- View and edit professor profiles
- Monitor search results

## Troubleshooting

### Common Issues

1. **API Key Errors**
   - Ensure `.env` file exists with correct keys
   - Verify API keys are valid and have quota remaining

2. **Empty Search Results**
   - Check API keys are configured
   - Try broader skill terms
   - Verify university/department data exists

3. **Dropdown Loading Issues**
   - Ensure JavaScript is enabled
   - Check browser console for errors
   - Verify AJAX endpoints are working

### Error Logging
Check terminal output for detailed error messages from API calls.

## Testing Endpoints

### Manual API Testing

#### Test Professor Search (POST)
```bash
curl -X POST http://127.0.0.1:8000/api/search/ \
  -H "Content-Type: application/json" \
  -d '{
    "country": "United States",
    "city": "Cambridge",
    "university": "MIT", 
    "department": "Computer Science",
    "skills": "artificial intelligence"
  }'
```

#### Test Location APIs (GET)
```bash
# Get all countries
curl http://127.0.0.1:8000/api/countries/

# Get cities for country ID 1
curl http://127.0.0.1:8000/api/cities/1/

# Get universities for city ID 1  
curl http://127.0.0.1:8000/api/universities/1/

# Get departments for university ID 1
curl http://127.0.0.1:8000/api/departments/1/
```

#### Test Professor Listing with Filters (GET)
```bash
curl "http://127.0.0.1:8000/api/professors/?university=MIT&skills=AI&page=1&page_size=5"
```

### Python Testing Scripts

#### Run Comprehensive Tests
```bash
python test.py
```

#### Test API Keys Only
```bash
python api_test.py
```

### Expected Response Formats

#### Location APIs Response (JSON)
```json
{
  "success": true,
  "countries": [
    {"id": 1, "name": "United States", "code": "USA"},
    {"id": 2, "name": "United Kingdom", "code": "GBR"}
  ]
}
```

#### Professor Search Response (JSON)
```json
{
  "success": true,
  "results_found": 5,
  "professors": [
    {
      "id": 1,
      "name": "Dr. John Smith",
      "email": "jsmith@mit.edu", 
      "portfolio_link": "https://www.mit.edu/~jsmith",
      "skills": "artificial intelligence, machine learning",
      "department": "Computer Science",
      "university": "MIT",
      "city": "Cambridge",
      "country": "United States",
      "created": true
    }
  ]
}
```

#### Professor List Response (JSON)
```json
{
  "success": true,
  "total_count": 25,
  "page": 1,
  "page_size": 10,
  "professors": [...]
}
```

## Deployment Notes

For production deployment:
- Set `DEBUG=False` in `.env`
- Use a production database (PostgreSQL recommended)
- Configure proper static file serving
- Set up SSL certificates
- Use environment variables for sensitive data

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

---

**Note**: This application requires active internet connection and valid API keys for Tavily and Groq services to function properly.
