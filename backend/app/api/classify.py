from fastapi import APIRouter
from pydantic import BaseModel

from app.services.classifier import doc_classifier
from app.services.preprocessor import preprocessing_pipeline

router = APIRouter()


class ClassifyRequest(BaseModel):
    text: str


class ClassifyResponse(BaseModel):
    category: str
    confidence: float
    top_categories: list[dict]


@router.post("/classify", response_model=ClassifyResponse)
async def classify_document(req: ClassifyRequest):
    preprocessed = preprocessing_pipeline.process(req.text)
    result = doc_classifier.classify(preprocessed.cleaned_text)
    return ClassifyResponse(
        category=result.category,
        confidence=result.confidence,
        top_categories=result.top_categories,
    )
