const LoadingSpinner = () => {
  return (
    <div className="flex justify-center items-center p-4">
      <div className="loading-container" style={{
        '--uib-size': '40px',
        '--uib-color': '#4F46E5',
        '--uib-speed': '0.9s'
      }}>
        <div className="loading-dot"></div>
        <div className="loading-dot"></div>
        <div className="loading-dot"></div>
        <div className="loading-dot"></div>
        <div className="loading-dot"></div>
        <div className="loading-dot"></div>
        <div className="loading-dot"></div>
        <div className="loading-dot"></div>
      </div>
    </div>
  );
};

export default LoadingSpinner;