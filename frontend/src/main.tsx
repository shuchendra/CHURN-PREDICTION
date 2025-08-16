import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.jsx';
import { UploadProvider } from './context/UploadContext';
import './index.css';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <UploadProvider>
      <App />
    </UploadProvider>
  </StrictMode>
);