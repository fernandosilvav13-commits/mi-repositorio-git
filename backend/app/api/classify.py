from fastapi import APIRouter
from pydantic import BaseModel

from app.services.classifier import doc_classifier
from app.schemas.classification import ClassificationResult

router = APIRouter()


class ClassifyRequest(BaseModel):
    text: str


class ClassifyResponse(BaseModel):
    category: str
    confidence: float
    top_categories: list[dict]


@router.post("/classify", response_model=ClassifyResponse)
async def classify_document(req: ClassifyRequest):
    result = doc_classifier.classify(req.text)
    return ClassifyResponse(
        category=result.category,
        confidence=result.confidence,
        top_categories=result.top_categories,
    )
