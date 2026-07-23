import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || "https://sentinelrag-production.up.railway.app/api/v1";

export interface ProcessingSummary {
    pages_processed: number;
    pages_with_text: number;
    pages_using_ocr: number;
    total_characters: number;
    processing_time_ms: number;
    processing_status: string;
}

export interface DocumentResponseData {
    document_id: string;
    filename: string;
    file_size: number;
    sha256: string;
    document_type: string;
    upload_timestamp: string;
    chunk_count: number;
    preview: string;
    processing_summary: ProcessingSummary;
}

export interface DocumentResponse {
    status: string;
    data: DocumentResponseData;
}

export const uploadDocument = async (file: File, onProgress?: (progressEvent: any) => void): Promise<DocumentResponse> => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post<DocumentResponse>(`${API_URL}/documents/upload`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: onProgress,
    });

    return response.data;
};
