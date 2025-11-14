import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import ObjectId
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import Homestay, Package, Booking

app = FastAPI(title="Ulin API", description="API for Ulin - Homestay & Tour Packages")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Ulin Backend Ready"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
    }
    try:
        if db is not None:
            response["database"] = "✅ Connected"
            response["collections"] = db.list_collection_names()
        else:
            response["database"] = "❌ Not Configured"
    except Exception as e:
        response["database"] = f"⚠️ Error: {str(e)[:80]}"
    return response

# ---------------------- Homestays ----------------------
@app.get("/homestays")
def list_homestays():
    items = get_documents("homestay")
    for it in items:
        it["id"] = str(it.pop("_id"))
    return items

@app.post("/homestays", status_code=201)
def create_homestay(payload: Homestay):
    try:
        _id = create_document("homestay", payload)
        return {"id": _id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------- Packages ----------------------
@app.get("/packages")
def list_packages():
    items = get_documents("package")
    for it in items:
        it["id"] = str(it.pop("_id"))
    return items

@app.post("/packages", status_code=201)
def create_package(payload: Package):
    try:
        _id = create_document("package", payload)
        return {"id": _id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------- Bookings ----------------------
@app.post("/bookings", status_code=201)
def create_booking(payload: Booking):
    try:
        _id = create_document("booking", payload)
        return {"id": _id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
