import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { UploadCloud, AlertCircle, Loader } from 'lucide-react';
import type { DocumentResponse } from '../services/uploadService';
import { uploadDocument } from '../services/uploadService';

interface DocumentUploadProps {
    onUploadSuccess: (data: DocumentResponse) => void;
}

export const DocumentUpload: React.FC<DocumentUploadProps> = ({ onUploadSuccess }) => {
    const [uploading, setUploading] = useState(false);
    const [progress, setProgress] = useState(0);
    const [error, setError] = useState<string | null>(null);

    const onDrop = useCallback(async (acceptedFiles: File[]) => {
        if (acceptedFiles.length === 0) return;

        const file = acceptedFiles[0];
        setUploading(true);
        setError(null);
        setProgress(0);

        try {
            const response = await uploadDocument(file, (progressEvent) => {
                if (progressEvent.total) {
                    const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                    setProgress(percentCompleted);
                }
            });
            onUploadSuccess(response);
        } catch (err: any) {
            setError(err.response?.data?.detail || err.message || 'An unexpected error occurred.');
        } finally {
            setUploading(false);
        }
    }, [onUploadSuccess]);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'application/pdf': ['.pdf']
        },
        maxFiles: 1,
        disabled: uploading
    });

    return (
        <div className="w-full max-w-2xl mx-auto mt-10">
            <div
                {...getRootProps()}
                className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-colors ${
                    isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400'
                } ${uploading ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
                <input {...getInputProps()} />
                <div className="flex flex-col items-center justify-center space-y-4">
                    {uploading ? (
                        <Loader className="w-12 h-12 text-blue-500 animate-spin" />
                    ) : (
                        <UploadCloud className="w-12 h-12 text-gray-400" />
                    )}
                    
                    <div className="text-lg font-medium text-gray-700">
                        {uploading ? 'Processing Document...' : (isDragActive ? 'Drop PDF here' : 'Drag & Drop PDF or Click to Browse')}
                    </div>
                    <p className="text-sm text-gray-500">Only .pdf files are supported (Max 10MB)</p>
                </div>
            </div>

            {uploading && progress > 0 && progress < 100 && (
                <div className="mt-6">
                    <div className="flex justify-between text-sm text-gray-600 mb-2">
                        <span>Uploading...</span>
                        <span>{progress}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2.5">
                        <div className="bg-blue-600 h-2.5 rounded-full" style={{ width: `${progress}%` }}></div>
                    </div>
                </div>
            )}

            {error && (
                <div className="mt-6 p-4 bg-red-50 rounded-lg flex items-start space-x-3 text-red-700">
                    <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
                    <div>
                        <h4 className="font-medium">Upload Failed</h4>
                        <p className="text-sm mt-1">{error}</p>
                    </div>
                </div>
            )}
        </div>
    );
};
