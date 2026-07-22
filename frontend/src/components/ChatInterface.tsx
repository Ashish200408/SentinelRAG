import React, { useState } from 'react';
import { queryChat } from '../services/chatService';
import type { ChatQueryResponse } from '../services/chatService';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { MessageSquare, Send, ChevronDown, ChevronUp, Loader2, AlertCircle, FileText, Activity } from 'lucide-react';

export const ChatInterface: React.FC = () => {
    const [question, setQuestion] = useState('');
    const [loading, setLoading] = useState(false);
    const [response, setResponse] = useState<ChatQueryResponse | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [showDecision, setShowDecision] = useState(false);

    const handleSubmit = async (e?: React.FormEvent) => {
        if (e) e.preventDefault();
        
        const trimmedQuestion = question.trim();
        if (!trimmedQuestion) return;

        setLoading(true);
        setError(null);
        setShowDecision(false);

        try {
            const data = await queryChat(trimmedQuestion);
            setResponse(data);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'An unexpected error occurred while fetching the answer.');
            setResponse(null);
        } finally {
            setLoading(false);
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter') {
            handleSubmit();
        }
    };

    return (
        <div className="w-full max-w-4xl mx-auto mt-8 bg-white border border-gray-200 rounded-lg shadow-sm overflow-hidden">
            <div className="p-6 bg-indigo-50 border-b border-gray-200 flex items-center">
                <MessageSquare className="w-6 h-6 text-indigo-600 mr-3" />
                <h3 className="text-xl font-semibold text-gray-900">Ask Questions</h3>
            </div>
            
            <div className="p-6 space-y-6">
                <form onSubmit={handleSubmit} className="flex space-x-3">
                    <input
                        type="text"
                        value={question}
                        onChange={(e) => setQuestion(e.target.value)}
                        onKeyDown={handleKeyDown}
                        placeholder="Ask a question about your uploaded document..."
                        className="flex-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 py-3 px-4 border"
                        disabled={loading}
                    />
                    <button
                        type="submit"
                        disabled={loading || !question.trim()}
                        className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Send className="w-5 h-5" />}
                        <span className="ml-2">{loading ? 'Asking...' : 'Ask'}</span>
                    </button>
                </form>

                {error && (
                    <div className="rounded-md bg-red-50 p-4 border border-red-200">
                        <div className="flex">
                            <div className="flex-shrink-0">
                                <AlertCircle className="h-5 w-5 text-red-400" aria-hidden="true" />
                            </div>
                            <div className="ml-3">
                                <h3 className="text-sm font-medium text-red-800">Error retrieving answer</h3>
                                <div className="mt-2 text-sm text-red-700">
                                    <p>{error}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                {response && (
                    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
                        {response.answer && (
                            <div className="p-5 bg-gray-50 rounded-lg border border-gray-200">
                                <h4 className="text-md font-semibold text-gray-900 mb-2">Answer</h4>
                                <div className="text-gray-800 prose prose-sm max-w-none">
                                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                        {response.answer}
                                    </ReactMarkdown>
                                </div>
                            </div>
                        )}

                        {response.clarification && (
                            <div className="p-5 bg-amber-50 rounded-lg border border-amber-200">
                                <h4 className="text-md font-semibold text-amber-900 mb-2 flex items-center">
                                    <AlertCircle className="w-5 h-5 mr-2" />
                                    Clarification
                                </h4>
                                <p className="text-amber-800 whitespace-pre-wrap leading-relaxed">{response.clarification}</p>
                            </div>
                        )}

                        {response.sources && response.sources.length > 0 && (
                            <div>
                                <h4 className="text-md font-semibold text-gray-900 mb-3 flex items-center">
                                    <FileText className="w-5 h-5 mr-2 text-gray-500" />
                                    Sources
                                </h4>
                                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                                    {response.sources.map((source, idx) => (
                                        <div key={idx} className="p-3 bg-white border border-gray-200 rounded-md shadow-sm flex flex-col">
                                            <span className="font-medium text-sm text-gray-900 truncate" title={source.filename}>
                                                {source.filename}
                                            </span>
                                            <div className="flex justify-between items-center mt-2 text-xs text-gray-500">
                                                <span>Similarity: {source.similarity_score.toFixed(3)}</span>
                                                {source.page_number && <span>Page: {source.page_number}</span>}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {response.decision && (
                            <div className="border border-gray-200 rounded-md overflow-hidden">
                                <button 
                                    onClick={() => setShowDecision(!showDecision)}
                                    className="w-full flex items-center justify-between p-4 bg-gray-50 hover:bg-gray-100 transition-colors focus:outline-none"
                                >
                                    <div className="flex items-center text-gray-700 font-medium">
                                        <Activity className="w-5 h-5 mr-2 text-indigo-500" />
                                        Decision Information
                                    </div>
                                    {showDecision ? <ChevronUp className="w-5 h-5 text-gray-500" /> : <ChevronDown className="w-5 h-5 text-gray-500" />}
                                </button>
                                
                                {showDecision && (
                                    <div className="p-4 bg-white border-t border-gray-200">
                                        <dl className="grid grid-cols-1 sm:grid-cols-2 gap-x-4 gap-y-4 text-sm">
                                            <div>
                                                <dt className="text-gray-500 mb-1">Path</dt>
                                                <dd className="font-medium text-gray-900 bg-gray-100 px-2 py-1 rounded inline-block">{response.decision.path}</dd>
                                            </div>
                                            <div>
                                                <dt className="text-gray-500 mb-1">Retrieval Quality</dt>
                                                <dd className="font-medium text-gray-900 bg-gray-100 px-2 py-1 rounded inline-block">{response.decision.retrieval_quality}</dd>
                                            </div>
                                            <div>
                                                <dt className="text-gray-500 mb-1">Confidence</dt>
                                                <dd className="font-medium text-gray-900">{response.decision.confidence.toFixed(3)}</dd>
                                            </div>
                                            <div>
                                                <dt className="text-gray-500 mb-1">Rewritten</dt>
                                                <dd className="font-medium text-gray-900">{response.decision.rewritten ? 'Yes' : 'No'}</dd>
                                            </div>
                                            <div>
                                                <dt className="text-gray-500 mb-1">Attempts</dt>
                                                <dd className="font-medium text-gray-900">{response.decision.retrieval_attempts}</dd>
                                            </div>
                                            {response.decision.rewritten_query && (
                                                <div className="sm:col-span-2">
                                                    <dt className="text-gray-500 mb-1">Rewritten Query</dt>
                                                    <dd className="font-medium text-gray-900 italic">"{response.decision.rewritten_query}"</dd>
                                                </div>
                                            )}
                                        </dl>
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
};
