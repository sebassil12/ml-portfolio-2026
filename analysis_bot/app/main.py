from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import sys
import os

# Add parent directory to path to allow imports from sibling directories
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper.browser import scrape_reviews
from services.llm import analyze_reviews
from services.db import supabase

app = FastAPI(title="The Pain Hunter API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    url: str
    platform: str = "amazon"

class AnalysisResult(BaseModel):
    status: str
    analysis_id: Optional[int] = None
    data: Dict[str, Any]

@app.get("/")
def read_root():
    return {"status": "ok", "message": "The Pain Hunter is ready to hunt."}

@app.post("/analyze", response_model=AnalysisResult)
async def analyze_url(request: AnalyzeRequest):
    try:
        # 1. Scrape Reviews
        print(f"Scraping URL: {request.url}")
        raw_text = await scrape_reviews(request.url)
        
        if not raw_text:
            raise HTTPException(status_code=400, detail="Failed to scrape content from URL")

        # 2. Analyze with LLM
        print("Analyzing content with LLM...")
        analysis_data = await analyze_reviews(raw_text)

        # 3. Save to Supabase
        analysis_id = None
        if supabase:
            try:
                data = {
                    "url": request.url,
                    "platform": request.platform,
                    "raw_text": raw_text[:10000], # Truncate to save space if needed, or store full
                    "analysis_json": analysis_data
                }
                response = supabase.table("analysis_results").insert(data).execute()
                if response.data:
                    analysis_id = response.data[0]['id']
            except Exception as e:
                print(f"Database error: {e}")
                # Continue even if DB fails, return result to user
        
        return {
            "status": "success",
            "analysis_id": analysis_id,
            "data": analysis_data
        }

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/results/{analysis_id}")
def get_analysis_result(analysis_id: int):
    if not supabase:
        raise HTTPException(status_code=503, detail="Database not configured")
        
    try:
        response = supabase.table("analysis_results").select("analysis_json").eq("id", analysis_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Analysis not found")
            
        return {
            "status": "success",
            "analysis_id": analysis_id,
            "data": response.data[0]['analysis_json']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
