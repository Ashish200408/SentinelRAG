import React from 'react';
import type { DocumentResponseData } from '../services/uploadService';
import { FileText, CheckCircle, Clock, Hash, AlignLeft, ShieldCheck } from 'lucide-react';
import { ChatInterface } from './ChatInterface';

interface DocumentResultsProps {
    data: DocumentResponseData;
    onReset: () => void;
}

export const DocumentResults: React.FC<DocumentResultsProps> = ({ data, onReset }) => {
    return (
        <div className="w-full max-w-4xl mx-auto mt-10 space-y-6">
            <div className="flex items-center justify-between p-6 bg-green-50 border border-green-200 rounded-lg">
                <div className="flex items-center space-x-4">
                    <CheckCircle className="w-8 h-8 text-green-500" />
                    <div>
                        <h2 className="text-xl font-semibold text-green-900">Upload Successful</h2>
                        <p className="text-green-700">{data.filename}</p>
                    </div>
                </div>
                <button 
                    onClick={onReset}
                    className="px-4 py-2 text-sm font-medium text-green-700 bg-green-100 rounded-md hover:bg-green-200"
                >
                    Upload Another
                </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="p-6 bg-white border border-gray-200 rounded-lg shadow-sm">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                        <FileText className="w-5 h-5 mr-2 text-gray-500" />
                        Metadata
                    </h3>
                    <dl className="space-y-3 text-sm">
                        <div className="flex justify-between">
                            <dt className="text-gray-500">Document ID</dt>
                            <dd className="font-mono text-gray-900 truncate ml-4">{data.document_id}</dd>
                        </div>
                        <div className="flex justify-between">
                            <dt className="text-gray-500">File Size</dt>
                            <dd className="font-medium text-gray-900">{(data.file_size / 1024).toFixed(2)} KB</dd>
                        </div>
                        <div className="flex justify-between">
                            <dt className="text-gray-500">Document Type</dt>
                            <dd className="font-medium text-gray-900">{data.document_type}</dd>
                        </div>
                        <div className="flex justify-between">
                            <dt className="text-gray-500">Timestamp</dt>
                            <dd className="font-medium text-gray-900">{new Date(data.upload_timestamp).toLocaleString()}</dd>
                        </div>
                    </dl>
                </div>

                <div className="p-6 bg-white border border-gray-200 rounded-lg shadow-sm">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                        <ShieldCheck className="w-5 h-5 mr-2 text-blue-500" />
                        Processing Summary
                    </h3>
                    <dl className="space-y-3 text-sm">
                        <div className="flex justify-between">
                            <dt className="text-gray-500 flex items-center"><Hash className="w-4 h-4 mr-1"/> Chunks Generated</dt>
                            <dd className="font-medium text-blue-600">{data.chunk_count}</dd>
                        </div>
                        <div className="flex justify-between">
                            <dt className="text-gray-500">Pages Processed</dt>
                            <dd className="font-medium text-gray-900">{data.processing_summary.pages_processed}</dd>
                        </div>
                        <div className="flex justify-between">
                            <dt className="text-gray-500">Pages with Text</dt>
                            <dd className="font-medium text-gray-900">{data.processing_summary.pages_with_text}</dd>
                        </div>
                        <div className="flex justify-between">
                            <dt className="text-gray-500">OCR Used (Pages)</dt>
                            <dd className="font-medium text-amber-600">{data.processing_summary.pages_using_ocr}</dd>
                        </div>
                        <div className="flex justify-between">
                            <dt className="text-gray-500 flex items-center"><Clock className="w-4 h-4 mr-1"/> Processing Time</dt>
                            <dd className="font-medium text-gray-900">{data.processing_summary.processing_time_ms} ms</dd>
                        </div>
                    </dl>
                </div>
            </div>

            <div className="p-6 bg-white border border-gray-200 rounded-lg shadow-sm">
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                    <AlignLeft className="w-5 h-5 mr-2 text-gray-500" />
                    Cleaned Text Preview (First 500 characters)
                </h3>
                <div className="p-4 bg-gray-50 rounded border border-gray-100 text-sm font-mono text-gray-800 whitespace-pre-wrap">
                    {data.preview || "No text could be extracted."}
                </div>
            </div>

            <ChatInterface />
        </div>
    );
};
