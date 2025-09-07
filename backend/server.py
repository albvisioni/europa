from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path

# Import database connection
from .database import connect_to_mongo, close_mongo_connection

# Import route modules
from .routes.auth import router as auth_router
from .routes.users import router as users_router
from .routes.countries import router as countries_router
from .routes.battles import router as battles_router
from .routes.companies import router as companies_router

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create the main app
app = FastAPI(
    title="Europa API",
    description="Browser-based strategy game API similar to eRepublik",
    version="1.0.0"
)

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Health check endpoint
@api_router.get("/")
async def root():
    return {"message": "Europa API is running", "version": "1.0.0"}

@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Europa API is operational"}

# Include all route modules
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(countries_router)
api_router.include_router(battles_router)
api_router.include_router(companies_router)

# Include the main router in the app
app.include_router(api_router)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Database connection events
@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()
    logger.info("Europa API started successfully")

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()
    logger.info("Europa API shut down")
