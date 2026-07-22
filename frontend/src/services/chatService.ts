const API_BASE_URL = 'http://localhost:8000/api/v1';

export interface SourceMetadata {
    document_id: string;
    filename: string;
    chunk_index: number;
    similarity_score: number;
    page_number?: number | null;
}

export interface DecisionMetadata {
    path: string;
    retrieval_quality: string;
    rewritten: boolean;
    rewritten_query?: string | null;
    retrieval_attempts: number;
    best_similarity: number;
    average_similarity: number;
    retrieved_chunks: number;
    confidence: number;
}

export interface ChatQueryResponse {
    answer?: string | null;
    clarification?: string | null;
    sources: SourceMetadata[];
    chunk_count: number;
    generation_time_ms: number;
    decision: DecisionMetadata;
}

export const queryChat = async (question: string): Promise<ChatQueryResponse> => {
    const response = await fetch(`${API_BASE_URL}/chat/query`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
    });

    if (!response.ok) {
        throw new Error(`Chat query failed: ${response.statusText}`);
    }

    return response.json();
};
