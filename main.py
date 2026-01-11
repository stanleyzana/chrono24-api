from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from chrono24 import query
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"status": "ok"}

@app.get("/search")
def search_watches(query_str: str = None, limit: int = 100):
    # Rename parameter to avoid conflict with chrono24.query
    search_query = query_str
    if not search_query:
        from fastapi import Query
        raise HTTPException(status_code=400, detail="query parameter is required")
    
    try:
        logger.info(f"Searching for: {search_query}")
        
        # Use the chrono24 library
        results = query(search_query)
        
        listings = []
        count = 0
        for watch in results:
            if count >= limit:
                break
            listings.append({
                "id": watch.id if hasattr(watch, 'id') else str(count),
                "title": watch.title if hasattr(watch, 'title') else "",
                "price": watch.price if hasattr(watch, 'price') else 0,
                "currency": "EUR",
                "url": watch.url if hasattr(watch, 'url') else "",
                "manufacturer": watch.manufacturer if hasattr(watch, 'manufacturer') else "",
                "model": watch.model if hasattr(watch, 'model') else "",
                "reference": watch.reference_number if hasattr(watch, 'reference_number') else "",
                "condition": watch.condition if hasattr(watch, 'condition') else "",
                "year": watch.year if hasattr(watch, 'year') else None,
                "image_url": watch.image_urls[0] if hasattr(watch, 'image_urls') and watch.image_urls else "",
                "location": watch.location if hasattr(watch, 'location') else "",
            })
            count += 1
        
        logger.info(f"Found {len(listings)} listings")
        return {"listings": listings, "total": len(listings)}
        
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
