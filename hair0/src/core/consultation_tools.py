"""
Tools for Hairstyle Consultation Agent

Core tools for requesting face photos, getting facial shape descriptions, and searching knowledge bases
"""

import logging
from strands import tool
import json
import requests

logger = logging.getLogger(__name__)


# not used, example code for doing this over Http without MCPs
@tool
def describe_face_shape(img_path: str) -> str:
    try:
        url = "http://0.0.0.0:8001/api/describe-face"
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(url, json={ 'imgPath': img_path }, headers=headers)
        response.raise_for_status()
        logger.info(f"API call successful: {response.json()}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error: {e}")
    return 'Something didnt work!'


@tool
def search_knowledge_base(query) -> str:
    """
    Search the knowledge base for relevant documents.
    
    Args:
        query: Search query
        max_results: Maximum number of results to return
        
    Returns:
        JSON string of search results
    """
    query_lower = query.lower()
    results = []
    
    for doc in KNOWLEDGE_BASE["documents"]:
        # Simple keyword matching
        score = 0
        
        # Check title
        if any(word in doc["title"].lower() for word in query_lower.split()):
            score += 3
            
        # Check content
        if any(word in doc["content"].lower() for word in query_lower.split()):
            score += 2
            
        # Check tags
        if any(word in " ".join(doc["tags"]).lower() for word in query_lower.split()):
            score += 1
            
        if score > 0:
            results.append({
                "document": doc,
                "relevance_score": score
            })
    
    # Sort by relevance and limit results
    results.sort(key=lambda x: x["relevance_score"], reverse=True)
    
    return json.dumps(results, indent=2)


# Simulated knowledge base
KNOWLEDGE_BASE = {
    "documents": [
        {
            "id": "doc1",
            "title": "Suitable haircuts for round face shapes",
            "content": "Round face shapes generally benefit from elongation from hairstyles with volume. Haircuts such as combovers, brushbacks, two-block, and textured fringes work well. It is advisable to stay away from styles like buzzcuts as it will make the face look rounder.",
            "tags": ["round face", "volume", "haircuts", "suitability"]
        },
        {
            "id": "doc2", 
            "title": "Suitable haircuts for square or heart face shapes",
            "content": "Square or heart face shapes generally are suitable with most hairstyles, though one should be careful of hairstyles with too much volume such as a quiff or pompadour. Otherwise hairstyles of varying length such as brushbacks, textured fringes, two-block, mullet, and even buzz-cuts are suitable.",
            "tags": ["round face", "heart face", "volume", "haircuts", "suitability"]
        },
    ]
}
