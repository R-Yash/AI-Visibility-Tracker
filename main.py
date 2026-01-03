from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel
from typing import List, Dict
from prompts import get_prompt_generator
import json
import re
load_dotenv()

client = genai.Client()

class Prompts(BaseModel):
    category: str
    prompts:  List[str]


def LLM_call(prompt:str, model:str ="gemini-2.5-flash"):
    response = client.models.generate_content(model=model, contents=prompt)
    return response.text

def generate_prompts(category: str, model: str = "gemini-2.5-flash") -> Dict:
    prompt = get_prompt_generator(category)
    
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": Prompts.model_json_schema(),
        })
    
    return json.loads(response.text)

def generate_search_results(prompt:str):
    grounding_tool = types.Tool(google_search=types.GoogleSearch())
    config = types.GenerateContentConfig(tools=[grounding_tool])

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=config,
    )

    return response

def calculate_ai_visibility(brands: List[str] ,prompts: List[str]):
    brand_metrics = {
        brand: {
            "appeared_in_x_prompts": 0,  
            "total_mentions": 0,         
            "visibility_score": 0.0,     
            "contexts": []        
        } 
        for brand in brands
    }
    prompt_breakdown = []

    for prompt in prompts:
        result = LLM_call(prompt=prompt, model='gemini-2.5-flash')
        
        found_brands = []
        for brand in brands:
            matches = list(re.finditer(rf"\b{re.escape(brand)}\b", result, re.IGNORECASE))
            if matches:
                found_brands.append(brand)
                brand_metrics[brand]["appeared_in_x_prompts"] += 1
                brand_metrics[brand]["total_mentions"] += len(matches)
                
                # Context extraction
                sentences = re.split(r'(?<=[.!?]) +', result)
                for sentence in sentences:
                    if brand.lower() in sentence.lower():
                        clean = sentence.strip().replace("\n", " ")
                        brand_metrics[brand]["contexts"].append(clean[:50] + "...")
        
        prompt_breakdown.append({
            "prompt": prompt,
            "brands_mentioned": found_brands,
            "response_preview": result[:50] + "..."
        })

    total = len(prompts)
    for brand, metrics in brand_metrics.items():
        if total > 0:
            metrics["visibility_score"] = (metrics["appeared_in_x_prompts"] / total) * 100

    return {"metrics": brand_metrics, "breakdown": prompt_breakdown, "total_prompts": total}

def calculate_ai_citation_score(brands: List[str], prompts: List[str]):
    total_valid_citations = 0
    citation_scores = {brand:0 for brand in brands}
    cited_pages = []

    for prompt in prompts:
        result = generate_search_results(prompt)
        if not result.candidates or not result.candidates[0].grounding_metadata:
            continue
    
        chunks = result.candidates[0].grounding_metadata.grounding_chunks

        for chunk in chunks:
            if chunk.web and chunk.web.uri:
                url = chunk.web.uri
                title = chunk.web.title or "No Title"
                total_valid_citations += 1
            
                cited_pages.append({"url": url, "title": title})

                for brand in brands:
                    if brand.lower() in url.lower() or brand.lower() in title.lower():
                        citation_scores[brand] += 1
    
    metrics = {}
    for brand, count in citation_scores.items():
        share = (count / total_valid_citations * 100) if total_valid_citations > 0 else 0
        metrics[brand] = {"raw_citations": count, "share_of_voice": round(share, 2)}
    
    return {"metrics": metrics, "top_pages": cited_pages}
