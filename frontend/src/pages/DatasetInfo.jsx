import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import LoadingSpinner from '../components/LoadingSpinner';
import EDASection from '../components/EDASection';
import { useUpload } from '../context/UploadContext';

const DatasetInfo = () => {
  const [info, setInfo] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const { filesUploaded } = useUpload();
  const navigate = useNavigate();

  useEffect(() => {
    if (!filesUploaded) {
      navigate('/');
      return;
    }

    const fetchDatasetInfo = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/dataset/info');
        if (response.ok) {
          const data = await response.text();
          setInfo(data);
        } else {
          setError('Failed to fetch dataset information');
        }
      } catch (err) {
        setError('Network error while fetching dataset information');
      } finally {
        setLoading(false);
      }
    };

    fetchDatasetInfo();
  }, [filesUploaded, navigate]);

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      
      <main className="flex-grow container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold text-gray-900 mb-6">Dataset Information</h1>
          
          {error ? (
            <div className="bg-red-50 p-4 rounded-md">
              <p className="text-red-700">{error}</p>
            </div>
          ) : loading ? (
            <LoadingSpinner />
          ) : (
            <>
              <div className="bg-white p-6 rounded-lg shadow-md prose max-w-none mb-8"
                   dangerouslySetInnerHTML={{ __html: info }} />
              <EDASection />
            </>
          )}
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default DatasetInfo;