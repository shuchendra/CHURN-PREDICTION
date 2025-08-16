import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import FileUpload from '../components/FileUpload';
import SampleDataset from '../components/SampleDataset';
import { FileText, BarChart } from 'lucide-react';
import { useUpload } from '../context/UploadContext';

const Home = () => {
  const navigate = useNavigate();
  const { filesUploaded, setFilesUploaded } = useUpload();

  const handleUploadSuccess = () => {
    setFilesUploaded(true);
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      
      <main className="flex-grow container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            Customer Churn Prediction Analysis
          </h1>
          
          <p className="text-gray-600 mb-8">
            Upload your dataset and documentation to analyze customer churn patterns.
            Our advanced analytics will help you understand the factors contributing
            to customer churn and provide actionable insights.
          </p>

          {!filesUploaded ? (
            <FileUpload onUploadSuccess={handleUploadSuccess} />
          ) : (
            <div className="space-y-4">
              <button
                onClick={() => navigate('/dataset-info')}
                className="w-full flex items-center justify-center px-4 py-2 border border-transparent
                         rounded-md shadow-sm text-sm font-medium text-white bg-green-600 
                         hover:bg-green-700 focus:outline-none focus:ring-2 
                         focus:ring-offset-2 focus:ring-green-500"
              >
                <FileText className="w-4 h-4 mr-2" />
                Get Dataset Info
              </button>

              <button
                onClick={() => navigate('/questions')}
                className="w-full flex items-center justify-center px-4 py-2 border border-transparent
                         rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 
                         hover:bg-blue-700 focus:outline-none focus:ring-2 
                         focus:ring-offset-2 focus:ring-blue-500"
              >
                <BarChart className="w-4 h-4 mr-2" />
                Generate Business Questions
              </button>

              <button
                onClick={() => setFilesUploaded(false)}
                className="w-full flex items-center justify-center px-4 py-2 border border-gray-300
                         rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white 
                         hover:bg-gray-50 focus:outline-none focus:ring-2 
                         focus:ring-offset-2 focus:ring-indigo-500"
              >
                Upload Different Files
              </button>
            </div>
          )}

          <SampleDataset />
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Home