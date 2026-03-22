from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import categories, insights, summary, transactions

app = FastAPI(title="Nudge", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transactions.router)
app.include_router(categories.router)
app.include_router(summary.router)
app.include_router(insights.router)


@app.get("/")
async def root():
    return {"name": "Nudge", "version": "1.0.0", "status": "running"}
