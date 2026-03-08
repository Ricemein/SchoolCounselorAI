# College Counselor AI - Frontend

Modern React frontend for the College Admissions AI Counselor web application.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation
```bash
npm install
```

### Development
```bash
npm run dev
```

Visit http://localhost:3000

### Build for Production
```bash
npm run build
```

Output will be in `dist/` directory.

### Preview Production Build
```bash
npm run preview
```

## 📁 Project Structure

```
src/
├── api/                 # API client and types
│   └── client.ts       # Axios-based API client
├── components/          # Reusable components
│   ├── Header.tsx      # Navigation header
│   └── Footer.tsx      # Page footer
├── pages/              # Page components (routes)
│   ├── HomePage.tsx           # Landing page
│   ├── ProfileAnalysis.tsx    # Profile analysis form
│   ├── UniversityMatcher.tsx  # University matching
│   ├── EssayCoach.tsx         # Essay feedback
│   ├── Timeline.tsx           # Timeline generator
│   └── ResearchFinder.tsx     # Research opportunities
├── App.tsx             # Main app with routing
├── main.tsx            # Application entry point
└── index.css           # Global styles (Tailwind)
```

## 🎨 Technologies

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **Lucide React** - Icon library

## 🔌 API Integration

The frontend connects to the FastAPI backend. Configure the API URL:

1. Copy `.env.example` to `.env`
2. Set `VITE_API_URL` to your backend URL
3. Restart dev server

Example:
```bash
VITE_API_URL=http://localhost:8000
```

For production:
```bash
VITE_API_URL=https://your-api-domain.com
```

## 🎨 Styling

### Tailwind CSS

Utility classes are used throughout. Common patterns:

```tsx
// Cards
<div className="card">...</div>

// Buttons
<button className="btn-primary">...</button>
<button className="btn-secondary">...</button>

// Inputs
<input className="input" />
<label className="label">...</label>
```

### Customization

Edit `tailwind.config.js` to customize theme:

```javascript
theme: {
  extend: {
    colors: {
      primary: {
        // Your brand colors
        500: '#3b82f6',
        600: '#2563eb',
        // ...
      },
    },
  },
}
```

## 📱 Pages

### Home Page (`/`)
Landing page with feature overview and call-to-action

### Profile Analysis (`/profile-analysis`)
Form for analyzing student academic profile

### University Matcher (`/university-matcher`)
Find CS/Engineering programs matching student profile

### Essay Coach (`/essay-coach`)
Submit essays for AI-powered feedback

### Timeline (`/timeline`)
Generate personalized application timeline

### Research Finder (`/research-finder`)
Discover research opportunities

## 🧩 Components

### Header
- Navigation menu
- Responsive mobile menu
- Branding

### Footer
- Links to pages
- Social media/contact info
- Copyright notice

### Reusable Patterns

All forms follow similar structure:
1. State management with `useState`
2. Form submission with loading states
3. Error handling
4. Results display

## 🚀 Deployment

### Vercel

```bash
npm i -g vercel
vercel --prod
```

Set environment variable:
- `VITE_API_URL`: Your backend API URL

### Netlify

1. Connect GitHub repository
2. Build command: `npm run build`
3. Publish directory: `dist`
4. Add environment variable: `VITE_API_URL`

### Docker

```bash
docker build -t counselor-frontend .
docker run -p 80:80 counselor-frontend
```

## 🧪 Development

### Code Quality

```bash
# Type checking
npm run build

# Linting
npm run lint
```

### Adding New Pages

1. Create component in `src/pages/`
2. Add route in `src/App.tsx`
3. Add navigation link in `src/components/Header.tsx`

Example:
```tsx
// src/pages/NewPage.tsx
export function NewPage() {
  return <div>New Page</div>;
}

// src/App.tsx
import { NewPage } from './pages/NewPage';
// ...
<Route path="/new-page" element={<NewPage />} />
```

### API Client

Add new API endpoints in `src/api/client.ts`:

```typescript
export const apiClient = {
  // Existing methods...
  
  newEndpoint: async (data: any) => {
    const response = await api.post('/api/new-endpoint', data);
    return response.data;
  },
};
```

## 📦 Building

### Development Build
```bash
npm run dev
```
- Hot module replacement
- Source maps
- Fast refresh

### Production Build
```bash
npm run build
```
- Minified code
- Optimized assets
- Tree shaking
- Code splitting

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Or use different port
npm run dev -- --port 3001
```

### Build Errors
```bash
# Clear cache
rm -rf node_modules .vite dist
npm install
npm run build
```

### API Connection Issues
1. Verify backend is running
2. Check `VITE_API_URL` in `.env`
3. Check browser console for CORS errors
4. Verify backend CORS settings

## 📚 Resources

- [React Documentation](https://react.dev)
- [Vite Documentation](https://vitejs.dev)
- [Tailwind CSS Documentation](https://tailwindcss.com)
- [React Router Documentation](https://reactrouter.com)

## 🤝 Contributing

1. Create feature branch
2. Make changes
3. Test thoroughly
4. Submit pull request

## 📄 License

MIT License
