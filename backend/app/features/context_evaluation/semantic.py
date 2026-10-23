import logging
import json
from pydantic import BaseModel, ValidationError
from app.providers.gemini.provider import gemini_provider

logger = logging.getLogger(__name__)

class SemanticEvaluationResult(BaseModel):
    answerable: bool
    confidence: float
    reason: str

class SemanticEvaluator:
    def evaluate(self, question: str, chunks_text: str) -> SemanticEvaluationResult | None:
        prompt = f"""Does the retrieved context contain sufficient evidence to answer the user's question?
Return your answer exactly as a JSON object with the following fields, and no other text:
- answerable: boolean true or false
- confidence: a float between 0.0 and 1.0 indicating your confidence
- reason: a concise evidence-based reason for your decision

Context:
{chunks_text}

Question:
{question}
"""
        try:
            # We use the generate_answer method since it calls Gemini
            response_text = gemini_provider.generate_answer(prompt)
            
            # Clean up the response if it has markdown formatting
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
                
            response_text = response_text.strip()
            
            data = json.loads(response_text)
            result = SemanticEvaluationResult(**data)
            return result
        except json.JSONDecodeError as e:
            logger.error(f"Semantic evaluation failed to parse JSON: {e}")
            return None
        except ValidationError as e:
            logger.error(f"Semantic evaluation returned invalid data structure: {e}")
            return None
        except Exception as e:
            logger.error(f"Semantic evaluation failed due to an exception: {e}")
            return None

semantic_evaluator = SemanticEvaluator()
