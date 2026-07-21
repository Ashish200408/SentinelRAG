import React, { useState } from 'react';
import { DocumentUpload } from '../components/DocumentUpload';
import { DocumentResults } from '../components/DocumentResults';
import type { DocumentResponse } from '../services/uploadService';

export const UploadPage: React.FC = () => {
    const [result, setResult] = useState<DocumentResponse | null>(null);

    return (
        <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-7xl mx-auto">
                <div className="text-center mb-12">
                    <h1 className="text-4xl font-extrabold text-gray-900 tracking-tight sm:text-5xl">
                        SentinelRAG Ingestion
                    </h1>
                    <p className="mt-4 max-w-2xl text-xl text-gray-500 mx-auto">
                        Upload your PDF documents to extract text, run OCR if necessary, and generate optimized chunks for retrieval.
                    </p>
                </div>

                {!result ? (
                    <DocumentUpload onUploadSuccess={setResult} />
                ) : (
                    <DocumentResults data={result.data} onReset={() => setResult(null)} />
                )}
            </div>
        </div>
    );
};
