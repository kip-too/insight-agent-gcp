from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import os
from typing import Dict, Any

app = FastAPI(
    title="Insight-Agent",
    description="AI-powered text analysis service",
    version="1.0.0"
)

class TextAnalysisRequest(BaseModel):
    text: str

class TextAnalysisResponse(BaseModel):
    original_text: str
    word_count: int
    character_count: int
    sentence_count: int
    analysis_metadata: Dict[str, Any]

@app.get("/")
async def root():
    return {"message": "Insight-Agent API is running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/analyze", response_model=TextAnalysisResponse)
async def analyze_text(request: TextAnalysisRequest):
    """
    Analyze text and return basic statistics
    """
    try:
        text = request.text.strip()
        
        if not text:
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        # Basic text analysis
        word_count = len(text.split())
        character_count = len(text)
        sentence_count = len([s for s in text.split('.') if s.strip()])
        
        # Additional analysis metadata
        analysis_metadata = {
            "has_uppercase": any(c.isupper() for c in text),
            "has_numbers": any(c.isdigit() for c in text),
            "unique_words": len(set(text.lower().split())),
            "avg_word_length": round(sum(len(word) for word in text.split()) / word_count, 2) if word_count > 0 else 0
        }
        
        return TextAnalysisResponse(
            original_text=text,
            word_count=word_count,
            character_count=character_count,
            sentence_count=sentence_count,
            analysis_metadata=analysis_metadata
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)