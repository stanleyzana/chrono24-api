from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import chrono24

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"status": "ok"}

@app.get("/search")
def search_watches(query: str, limit: int = 100):
    try:
        results = []
        search = chrono24.query(query)
        
        for listing in search.search(limit=limit):
            results.append(listing)
        
        return {
            "success": True,
            "count": len(results),
            "total": search.count,
            "url": search.url,
            "listings": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
