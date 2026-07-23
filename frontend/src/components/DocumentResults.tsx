import React from 'react';
import type { DocumentResponseData } from '../services/uploadService';
import { FileText, CheckCircle, Clock, Hash, AlignLeft, ShieldCheck } from 'lucide-react';
import { ChatInterface } from './ChatInterface';
import { motion } from 'framer-motion';

interface DocumentResultsProps {
    data: DocumentResponseData;
    onReset: () => void;
}

export const DocumentResults: React.FC<DocumentResultsProps> = ({ data, onReset }) => {
    return (
        <motion.div initial={{ opacity: 0, scale: 0.98 }} animate={{ opacity: 1, scale: 1 }} className="w-full max-w-4xl mx-auto mt-10 space-y-6">
            <div className="flex items-center justify-between p-6 bg-gradient-to-r from-green-500 to-emerald-600 rounded-2xl shadow-lg text-white">
                <div className="flex items-center space-x-4">
                    <div className="w-12 h-12 bg-white/20 backdrop-blur-sm rounded-full flex items-center justify-center">
                        <CheckCircle className="w-6 h-6 text-white" />
                    </div>
                    <div>
                        <h2 className="text-xl font-bold text-white">Upload Successful</h2>
                        <p className="text-green-50 text-sm font-medium">{data.filename}</p>
                    </div>
                </div>
                <button 
                    onClick={onReset}
                    className="px-5 py-2.5 text-sm font-semibold text-green-700 bg-white rounded-xl hover:bg-green-50 transition-colors shadow-sm"
                >
                    Upload Another
                </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="p-6 glass-card rounded-2xl">
                    <h3 className="text-lg font-bold text-gray-900 mb-6 flex items-center">
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

                <div className="p-6 glass-card rounded-2xl">
                    <h3 className="text-lg font-bold text-gray-900 mb-6 flex items-center">
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

            <div className="p-6 glass-card rounded-2xl">
                <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center">
                    <AlignLeft className="w-5 h-5 mr-2 text-gray-500" />
                    Cleaned Text Preview (First 500 characters)
                </h3>
                <div className="p-4 bg-gray-50 rounded border border-gray-100 text-sm font-mono text-gray-800 whitespace-pre-wrap">
                    {data.preview || "No text could be extracted."}
                </div>
            </div>

            <ChatInterface />
        </motion.div>
    );
};
