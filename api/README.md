# API Server

FastAPI backend for the College Admissions AI Counselor web application.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   ```bash
   cp ../.env.example .env
   # Edit .env with your configuration
   ```

3. **Run the server:**
   ```bash
   python server.py
   ```

   Or with uvicorn directly:
   ```bash
   uvicorn server:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Access the API:**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

## API Endpoints

### Health Check
- `GET /` - Basic health check
- `GET /api/health` - Detailed health status

### Student Profile
- `POST /api/analyze-profile` - Analyze student profile
- `POST /api/suggest-essay-topics` - Get essay topic suggestions
- `POST /api/generate-timeline` - Generate application timeline
- `POST /api/find-research-opportunities` - Find research opportunities

### University Matching
- `POST /api/match-universities` - Find matching universities
- `GET /api/universities` - List all universities

### Essay Analysis
- `POST /api/analyze-essay` - Analyze essay and get feedback

## Example Request

```bash
curl -X POST "http://localhost:8000/api/analyze-profile" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "graduation_year": 2025,
    "academic_record": {
      "gpa": 3.9,
      "sat_total": 1520,
      "ap_courses": ["AP Computer Science A", "AP Calculus BC"]
    },
    "cs_interests": ["AI/ML", "Robotics"]
  }'
```

## Deployment

### Railway
1. Install Railway CLI: `npm i -g @railway/cli`
2. Login: `railway login`
3. Initialize: `railway init`
4. Deploy: `railway up`

### Render
1. Create new Web Service
2. Connect GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn server:app --host 0.0.0.0 --port $PORT`

### Heroku
1. Install Heroku CLI
2. Create app: `heroku create your-app-name`
3. Deploy: `git push heroku main`

## Environment Variables

Required:
- `OPENAI_API_KEY` - Your OpenAI API key (if using OpenAI)
- `USE_LOCAL_MODEL` - Set to `true` for local models (optional)

Optional:
- `LOCAL_MODEL` - HuggingFace model name
- `TEMPERATURE` - LLM temperature (default: 0.7)
- `MAX_TOKENS` - Max tokens per response (default: 2000)

## CORS Configuration

Update `allow_origins` in `server.py` for production:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    ...
)
```
