import { UploadPage } from './pages/UploadPage';
import { Sparkles } from 'lucide-react';

function App() {
  return (
    <div className="flex flex-col min-h-screen bg-[#fafafa] text-gray-900 overflow-hidden selection:bg-indigo-500/30">
      <div className="w-full bg-white/80 backdrop-blur-md border-b border-gray-200/50 flex items-center px-6 py-4 fixed top-0 z-50">
        <div className="flex items-center space-x-2">
          <div className="w-8 h-8 rounded-xl bg-indigo-600 flex items-center justify-center">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <h1 className="text-xl font-bold tracking-tight text-gray-900">SentinelRAG</h1>
        </div>
      </div>
      <main className="flex-1 overflow-y-auto pt-16">
        <UploadPage />
      </main>
    </div>
  );
}

export default App;
