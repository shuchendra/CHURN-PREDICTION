import { createContext, useContext, useState } from 'react';

const UploadContext = createContext();

export const useUpload = () => {
  const context = useContext(UploadContext);
  if (!context) {
    throw new Error('useUpload must be used within an UploadProvider');
  }
  return context;
};

export const UploadProvider = ({ children }) => {
  const [filesUploaded, setFilesUploaded] = useState(false);

  return (
    <UploadContext.Provider value={{ filesUploaded, setFilesUploaded }}>
      {children}
    </UploadContext.Provider>
  );
};