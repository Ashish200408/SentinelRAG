import React, { useState } from 'react';
import { DocumentUpload } from '../components/DocumentUpload';
import { DocumentResults } from '../components/DocumentResults';
import type { DocumentResponse } from '../services/uploadService';

export const UploadPage: React.FC = () => {
    const [result, setResult] = useState<DocumentResponse | null>(null);

    return (
        <div className="w-full max-w-5xl mx-auto py-12 px-4 sm:px-6 lg:px-8 flex-1 flex flex-col h-full justify-center">
            <div className="w-full">
                <div className="text-center mb-16">
                    <h1 className="text-4xl md:text-5xl font-bold tracking-tight text-gray-900 mb-4">
                        Document Intelligence
                    </h1>
                    <p className="max-w-2xl text-lg text-gray-500 mx-auto">
                        Upload your PDF documents to extract text, run OCR if necessary, and generate optimized chunks for AI retrieval.
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
