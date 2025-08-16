import { useState } from 'react';
import { Upload } from 'lucide-react';

const FileUpload = ({ onUploadSuccess }) => {
  const [dataset, setDataset] = useState(null);
  const [documentation, setDocumentation] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!dataset || !documentation) {
      setError('Please select both dataset and documentation files');
      return;
    }

    setUploading(true);
    setError('');

    const formData = new FormData();
    formData.append('dataset', dataset);
    formData.append('documentation', documentation);

    try {
      const response = await fetch('http://127.0.0.1:8000/upload', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        onUploadSuccess();
      } else {
        setError('Upload failed. Please try again.');
      }
    } catch (err) {
      setError('Network error. Please check your connection.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <form onSubmit={handleUpload} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Dataset File</label>
          <input
            type="file"
            onChange={(e) => setDataset(e.target.files[0])}
            className="mt-1 block w-full text-sm text-gray-500
                      file:mr-4 file:py-2 file:px-4
                      file:rounded-md file:border-0
                      file:text-sm file:font-semibold
                      file:bg-indigo-50 file:text-indigo-700
                      hover:file:bg-indigo-100"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Documentation File</label>
          <input
            type="file"
            onChange={(e) => setDocumentation(e.target.files[0])}
            className="mt-1 block w-full text-sm text-gray-500
                      file:mr-4 file:py-2 file:px-4
                      file:rounded-md file:border-0
                      file:text-sm file:font-semibold
                      file:bg-indigo-50 file:text-indigo-700
                      hover:file:bg-indigo-100"
          />
        </div>

        {error && <p className="text-red-500 text-sm">{error}</p>}

        <button
          type="submit"
          disabled={uploading}
          className="w-full flex items-center justify-center px-4 py-2 border border-transparent
                   rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 
                   hover:bg-indigo-700 focus:outline-none focus:ring-2 
                   focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
        >
          {uploading ? (
            'Uploading...'
          ) : (
            <>
              <Upload className="w-4 h-4 mr-2" />
              Upload Files
            </>
          )}
        </button>
      </form>
    </div>
  );
};

export default FileUpload;