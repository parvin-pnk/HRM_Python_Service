from fastapi import FastAPI
from contextlib import asynccontextmanager


from services.ai_assistant.router import router as ai_router
from services.bug_analyzer.router import router as bug_router
from services.bug_analyzer.model_loader import load_models
from services.candidate_ranking.router import router as ranking_router
from services.candidate_ranking.model_loader import load_models
from services.insights_engineer.router import router as insights_router
from services.insights_engineer.model_loader import load_models
from services.ocr_verifier.router import router as ocr_router
from services.resume_parser.router import router as resume_router
from services.resume_parser.model_loader import load_models
from services.sprint_planner.router import router as sprint_router
from services.task_estimator.router import router as task_router
from services.task_estimator.model_loader import load_models




@asynccontextmanager
async def lifespan(app: FastAPI):
    load_models()
    yield

app = FastAPI(
    title="AI Layer",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(ai_router)
app.include_router(bug_router)
app.include_router(ranking_router)
app.include_router(insights_router)
app.include_router(ocr_router)
app.include_router(resume_router)
app.include_router(sprint_router)
app.include_router(task_router)