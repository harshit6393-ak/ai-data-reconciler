from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types
import json
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="Vision Reconciliation API")

# Allow React to talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# NEW: The endpoint now accepts Form data (text) and a File (image)
@app.post("/api/reconcile-vision")
async def reconcile_vision(
    record_a: str = Form(...), 
    receipt_image: UploadFile = File(...)
):
    try:
        # 1. Read the raw image bytes from the frontend
        image_bytes = await receipt_image.read()
        
        # 2. Instruct the AI to act as a multimodal auditor
        prompt = f"""
        You are an expert data auditor performing multimodal data reconciliation.
        Compare the provided digital Record A (JSON text) with the uploaded physical receipt image.
        Determine if they represent the exact same transaction.
        
        Record A: {record_a}
        
        Return ONLY a valid JSON object with no markdown formatting. The JSON must have these exact keys:
        "is_match": boolean,
        "confidence_score": integer from 1 to 100,
        "explanation": a short string detailing exactly what you see in the image vs the JSON.
        """
        
        # 3. Send BOTH the image bytes and the text prompt to Gemini
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type=receipt_image.content_type),
                prompt
            ]
        )
        
        # 4. Clean and return the output
        clean_text = response.text.strip().replace('```json', '').replace('```', '')
        result_json = json.loads(clean_text)
        return result_json
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vision reconciliation failed: {str(e)}")