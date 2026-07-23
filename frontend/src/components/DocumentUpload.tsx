import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { UploadCloud, AlertCircle, Loader } from 'lucide-react';
import type { DocumentResponse } from '../services/uploadService';
import { uploadDocument } from '../services/uploadService';
import { motion, AnimatePresence } from 'framer-motion';

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
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="w-full max-w-2xl mx-auto mt-10">
            <div
                {...getRootProps()}
                className={`border-2 border-dashed rounded-3xl p-16 text-center cursor-pointer transition-all duration-300 relative overflow-hidden group ${
                    isDragActive ? 'border-indigo-500 bg-indigo-50/50 shadow-lg scale-[1.02]' : 'border-gray-200 hover:border-indigo-400 glass-card'
                } ${uploading ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
                <input {...getInputProps()} />
                <div className="flex flex-col items-center justify-center space-y-6 relative z-10">
                    <div className="w-20 h-20 bg-indigo-50 rounded-2xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300 shadow-sm border border-indigo-100">
                        {uploading ? (
                            <Loader className="w-10 h-10 text-indigo-500 animate-spin" />
                        ) : (
                            <UploadCloud className="w-10 h-10 text-indigo-600" />
                        )}
                    </div>
                    
                    <div>
                        <h3 className="text-xl font-semibold text-gray-900 mb-2">
                            {uploading ? 'Processing Document...' : (isDragActive ? 'Drop PDF here' : 'Drop your PDF here')}
                        </h3>
                        <p className="text-sm text-gray-500">
                            Drag & drop or click to browse (Max 10MB)
                        </p>
                    </div>
                </div>
            </div>

            <AnimatePresence>
                {uploading && progress > 0 && progress < 100 && (
                    <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} exit={{ opacity: 0, height: 0 }} className="mt-8">
                        <div className="flex justify-between text-xs font-medium text-gray-500 mb-2">
                            <span>Uploading...</span>
                            <span>{progress}%</span>
                        </div>
                        <div className="w-full bg-gray-100 rounded-full h-2 overflow-hidden">
                            <motion.div 
                                className="bg-indigo-600 h-full rounded-full" 
                                initial={{ width: 0 }} 
                                animate={{ width: `${progress}%` }} 
                            />
                        </div>
                    </motion.div>
                )}

                {error && (
                    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="mt-6 p-4 glass-card bg-red-50/50 border border-red-100 rounded-2xl flex items-start space-x-3 text-red-700">
                        <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
                        <div>
                            <h4 className="font-semibold text-sm">Upload Failed</h4>
                            <p className="text-sm mt-1">{error}</p>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </motion.div>
    );
};
