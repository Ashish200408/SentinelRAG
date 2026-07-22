from app.providers.gemini.provider import gemini_provider

class QueryRewriteService:
    def rewrite(self, query: str) -> str:
        prompt = f"""Rewrite ONLY the search query to improve semantic retrieval.

Rules:
- Preserve user intent.
- Expand abbreviations where appropriate.
- Add relevant search keywords.
- Do NOT answer the question.
- Return ONLY the rewritten query.
- Do NOT include explanations.
- Output a single line.

Original Query: {query}
"""
        response = gemini_provider.generate_answer(prompt)
        return response.strip()

query_rewrite_service = QueryRewriteService()
