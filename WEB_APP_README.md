# College Counselor AI - Web Application

A modern, full-stack web application for AI-powered college admissions counseling focused on computer science and engineering programs.

## 🌐 Live Demo

- **Frontend**: Deploy to Vercel, Netlify, or any static hosting
- **Backend API**: Deploy to Railway, Render, or Heroku

## 📋 Features

### Student Features
- **Profile Analysis**: Comprehensive evaluation of academic credentials
- **University Matcher**: Find best-fit CS/Engineering programs
- **Essay Coach**: AI-powered essay feedback and topic suggestions
- **Timeline Generator**: Personalized application timeline
- **Research Finder**: Discover relevant research opportunities

### Technical Features
- Modern React frontend with TypeScript
- FastAPI backend with Python 3.12
- Responsive design with Tailwind CSS
- RESTful API architecture
- Docker support for easy deployment
- Multiple deployment options

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ (for frontend)
- Python 3.12+ (for backend)
- npm or yarn

### Local Development

#### 1. Start the Backend
```bash
# Navigate to API directory
cd api

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp ../.env.example .env
# Edit .env with your API keys

# Run the server
python server.py
```

Backend will be available at: http://localhost:8000

#### 2. Start the Frontend
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Set up environment
cp .env.example .env

# Run development server
npm run dev
```

Frontend will be available at: http://localhost:3000

### Using Docker Compose (Recommended)

```bash
# From the project root
docker-compose up --build
```

This will start both frontend and backend:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📦 Project Structure

```
Nish/
├── api/                          # FastAPI Backend
│   ├── server.py                 # Main API server
│   ├── requirements.txt          # Python dependencies
│   ├── Dockerfile               # API container config
│   └── README.md                # API documentation
├── frontend/                     # React Frontend
│   ├── src/
│   │   ├── api/                 # API client
│   │   ├── components/          # Reusable components
│   │   ├── pages/               # Page components
│   │   ├── App.tsx              # Main app component
│   │   └── main.tsx             # Entry point
│   ├── public/                  # Static assets
│   ├── package.json             # Node dependencies
│   ├── vite.config.ts           # Vite configuration
│   ├── tailwind.config.js       # Tailwind CSS config
│   ├── Dockerfile               # Frontend container
│   └── nginx.conf               # Nginx configuration
├── counselor_ai/                # Core AI logic
├── docker-compose.yml           # Docker orchestration
├── render.yaml                  # Render deployment config
└── README.md                    # This file
```

## 🌐 Deployment

### Deploy to Vercel (Frontend)

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Deploy:**
   ```bash
   cd frontend
   vercel --prod
   ```

3. **Set environment variables:**
   - `VITE_API_URL`: Your backend API URL

### Deploy to Netlify (Frontend)

1. **Connect your GitHub repository**
2. **Configure build settings:**
   - Build command: `cd frontend && npm run build`
   - Publish directory: `frontend/dist`
3. **Add environment variables:**
   - `VITE_API_URL`: Your backend API URL

### Deploy to Railway (Backend)

1. **Install Railway CLI:**
   ```bash
   npm i -g @railway/cli
   ```

2. **Login and deploy:**
   ```bash
   railway login
   cd api
   railway init
   railway up
   ```

3. **Set environment variables:**
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `USE_LOCAL_MODEL`: true/false
   - `PYTHON_VERSION`: 3.12.0

### Deploy to Render (Full Stack)

1. **Fork/Clone this repository**
2. **Connect to Render:**
   - Go to [render.com](https://render.com)
   - Click "New" → "Blueprint"
   - Connect your repository
   - Render will auto-detect `render.yaml`

3. **Set environment variables** in Render dashboard:
   - `OPENAI_API_KEY`
   - `USE_LOCAL_MODEL`

### Deploy with Docker

1. **Build and push to registry:**
   ```bash
   # Build images
   docker-compose build
   
   # Tag for your registry
   docker tag nish-frontend your-registry/counselor-frontend
   docker tag nish-api your-registry/counselor-api
   
   # Push to registry
   docker push your-registry/counselor-frontend
   docker push your-registry/counselor-api
   ```

2. **Deploy to your hosting platform** (AWS, GCP, Azure, DigitalOcean, etc.)

## 🔧 Configuration

### Backend Environment Variables
```bash
# Required (choose one)
OPENAI_API_KEY=sk-...              # For OpenAI API
USE_LOCAL_MODEL=true               # For local models

# Optional
LOCAL_MODEL=TinyLlama/TinyLlama-1.1B-Chat-v1.0
TEMPERATURE=0.7
MAX_TOKENS=2000
```

### Frontend Environment Variables
```bash
VITE_API_URL=http://localhost:8000  # Backend API URL
```

## 🧪 Testing

### Backend
```bash
cd api
pytest
```

### Frontend
```bash
cd frontend
npm test
```

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

- `POST /api/analyze-profile` - Analyze student profile
- `POST /api/match-universities` - Find matching universities
- `POST /api/analyze-essay` - Get essay feedback
- `POST /api/generate-timeline` - Create application timeline
- `POST /api/find-research-opportunities` - Find research opportunities
- `GET /api/universities` - List all universities

## 🎨 Customization

### Styling
The frontend uses Tailwind CSS. Customize colors in `frontend/tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      primary: {
        // Your custom colors
      },
    },
  },
}
```

### Adding Universities
Add universities to `counselor_ai/knowledge/universities.json`

### Modifying AI Prompts
Edit prompts in `counselor_ai/knowledge/prompts.py`

## 🔒 Security Best Practices

### Production Deployment

1. **Update CORS settings** in `api/server.py`:
   ```python
   allow_origins=["https://your-frontend-domain.com"]
   ```

2. **Use environment variables** for all secrets
3. **Enable HTTPS** on both frontend and backend
4. **Use rate limiting** for API endpoints
5. **Validate all user inputs**
6. **Regular dependency updates**

## 🐛 Troubleshooting

### Backend Issues

**Connection Refused:**
- Verify backend is running on port 8000
- Check firewall settings

**OpenAI API Errors:**
- Verify API key is correct
- Check API quota/billing
- Consider using local model as fallback

**Import Errors:**
- Ensure all dependencies installed: `pip install -r requirements.txt`
- Check Python version (3.12+)

### Frontend Issues

**API Connection Failed:**
- Verify `VITE_API_URL` is correct
- Check backend is running
- Check CORS settings

**Build Errors:**
- Clear node_modules: `rm -rf node_modules && npm install`
- Clear build cache: `rm -rf dist .vite`

**Type Errors:**
- Run type check: `npm run build`
- Update TypeScript: `npm install -D typescript@latest`

### Docker Issues

**Container Won't Start:**
- Check logs: `docker-compose logs`
- Verify environment variables set
- Ensure ports 3000 and 8000 are available

## 📄 License

MIT License - see LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for details

## 📧 Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/Ricemein/SchoolCounselorAI/issues)
- **Email**: support@collegecounselorai.com
- **Documentation**: See `/docs` folder

## 🌟 Acknowledgments

- Built with modern web technologies
- AI powered by OpenAI GPT-4 and HuggingFace transformers
- UI components inspired by best practices in React development

---

**Ready to deploy?** Choose your deployment method above and get started! 🚀
