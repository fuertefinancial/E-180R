from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
import chromadb
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="E-180R Email Automation API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

# Request model
class EmailRequest(BaseModel):
    email_content: str

# Response model
class EmailResponse(BaseModel):
    response: str

# Character persona for the AI assistant - "ideal for the normal"
CHARACTER_PERSONA = """You are a helpful and professional email assistant representing a financial technology company. Your tone should be:
- Professional yet approachable
- Clear and concise
- Helpful and solution-oriented
- Warm but not overly casual
- "Ideal for the normal" - meaning you communicate in a way that's accessible to everyone

Remember: You're helping with routine business communications like quotes, general inquiries, and standard customer service matters."""

@app.get("/")
async def root():
    return {"message": "E-180R Email Automation API is running"}

@app.post("/api/generate", response_model=EmailResponse)
async def generate_response(request: EmailRequest) -> Dict[str, str]:
    """
    Generate a professional response to an incoming email.
    """
    try:
        # Validate the incoming email content
        if not request.email_content or not request.email_content.strip():
            raise HTTPException(status_code=400, detail="Email content cannot be empty")
        
        # Load the ChromaDB collection
        try:
            collection = chroma_client.get_collection(name="company_knowledge")
        except Exception as e:
            # If collection doesn't exist, return error
            raise HTTPException(
                status_code=500, 
                detail="Knowledge base not initialized. Please run seed_database.py first."
            )
        
        # Perform similarity search to get top 2 most relevant documents
        results = collection.query(
            query_texts=[request.email_content],
            n_results=2
        )
        
        # Extract the relevant context from search results
        context_documents = []
        if results and results['documents'] and len(results['documents'][0]) > 0:
            context_documents = results['documents'][0]
        
        # Build the context string
        context = "Relevant company information:\n"
        for i, doc in enumerate(context_documents, 1):
            context += f"- {doc}\n"
        
        # Check if Gemini API is configured
        if not GEMINI_API_KEY:
            # Return placeholder response if API key not configured
            combined_text = f"{CHARACTER_PERSONA}\n\n{context}\n\nEmail to respond to:\n{request.email_content}"
            return {"response": f"PROCESSED (No API Key): {combined_text}"}
        
        # Construct the final prompt for Gemini
        prompt = f"""{CHARACTER_PERSONA}

{context}

Based on the provided context and your persona, draft a professional and helpful response to the following email. 
Make sure your response is complete, addresses all questions or concerns, and maintains a professional yet approachable tone.

Customer Email:
{request.email_content}

Your Response:"""

        # Generate response using Gemini
        response = model.generate_content(prompt)
        
        # Return the generated response
        return {"response": response.text}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 