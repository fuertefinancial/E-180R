# E-180R - AI-Powered Email Automation

E-180R is an intelligent email automation system designed to handle routine professional email communication for financial technology companies. It uses AI to generate contextually appropriate responses while maintaining a professional yet approachable tone.

## Features

- 🤖 AI-powered email response generation
- 📚 Vector database for company knowledge
- 🎯 Context-aware responses using ChromaDB
- 💬 "Ideal for the normal" character persona
- 🚀 Fast and scalable serverless architecture
- 🔒 Secure handling of sensitive information

## Tech Stack

- **Frontend**: React + Vite + Tailwind CSS
- **Backend**: FastAPI + Python
- **Vector Database**: ChromaDB
- **AI Model**: Google Gemini Pro (free tier)
- **Deployment**: GitHub Pages (frontend) + Vercel (backend)

## Prerequisites

- Node.js 20+ and npm
- Python 3.8+
- Google AI Studio API key (free)

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/E-180R.git
cd E-180R
```

### 2. Frontend Setup

```bash
cd frontend
npm install
```

Create a `.env` file in the frontend directory:
```
VITE_API_URL=http://localhost:8000
```

### 3. Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file in the backend directory:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

Get your free API key from: https://makersuite.google.com/app/apikey

### 4. Initialize the Knowledge Base

```bash
cd backend
python seed_database.py
```

This will create and populate the ChromaDB vector database with sample company knowledge.

### 5. Run the Application

**Backend** (in one terminal):
```bash
cd backend
uvicorn main:app --reload
```

**Frontend** (in another terminal):
```bash
cd frontend
npm run dev
```

Visit http://localhost:5173 to use the application.

## Usage

1. Paste an incoming email in the left textarea
2. Click "Generate Response"
3. The AI will analyze the email, search relevant company information, and generate a professional response
4. Copy the response and use it in your email client

## Deployment

### Frontend (GitHub Pages)

1. Push your code to GitHub
2. Enable GitHub Pages in repository settings
3. Set `VITE_API_URL` secret in GitHub Actions to your backend URL
4. The frontend will automatically deploy on push to main branch

### Backend (Vercel)

1. Install Vercel CLI: `npm i -g vercel`
2. Run `vercel` in the backend directory
3. Set the `GEMINI_API_KEY` environment variable in Vercel dashboard
4. Deploy with `vercel --prod`

## Project Structure

```
E-180R/
├── frontend/               # React frontend
│   ├── src/
│   │   ├── App.jsx        # Main application component
│   │   └── index.css      # Tailwind CSS styles
│   └── package.json
├── backend/               # FastAPI backend
│   ├── main.py           # API endpoints
│   ├── seed_database.py  # Database initialization
│   ├── requirements.txt  # Python dependencies
│   └── vercel.json      # Vercel configuration
└── .github/
    └── workflows/
        └── deploy.yml    # GitHub Actions workflow
```

## API Endpoints

- `GET /` - Health check
- `POST /api/generate` - Generate email response

### Request Format
```json
{
  "email_content": "Customer email text here..."
}
```

### Response Format
```json
{
  "response": "Generated professional response..."
}
```

## Security Considerations

- Never commit `.env` files with API keys
- Use environment variables for sensitive data
- The system is designed for routine emails only
- Sensitive emails should be handled manually

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## License

This project is proprietary to Fuerte Financial Technologies.

## Support

For issues or questions, please contact the development team. 