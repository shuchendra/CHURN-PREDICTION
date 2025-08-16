import { useState } from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';

const EDASection = () => {
  const [columnsData, setColumnsData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedColumn, setSelectedColumn] = useState(null);
  const [processingColumn, setProcessingColumn] = useState(false);

  const numericalStrategies = [
    "Replace with mean",
    "Replace with median",
    "Replace with mode",
    "Interpolate",
    "Forward fill (ffill)",
    "Backward fill (bfill)",
    "Drop rows"
  ];

  const categoricalStrategies = [
    "Replace with mode",
    "Forward fill (ffill)",
    "Backward fill (bfill)",
    "Drop rows"
  ];

  const fetchColumnsTypes = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/eda/columns-types');
      if (response.ok) {
        const data = await response.json();
        setColumnsData(data.columns);
      }
    } catch (error) {
      console.error('Error fetching columns:', error);
    }
    setLoading(false);
  };

  const handleStrategyClick = async (column, strategy) => {
    setProcessingColumn(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/eda/handle-nulls', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          column,
          strategy: strategy.toLowerCase(),
        }),
      });

      if (response.ok) {
        const data = await response.json();
        console.log(data)
        alert(data.message);
        setSelectedColumn(null);
      } else {
        const error = await response.json();
        alert(error.error || 'Failed to process strategy');
      }
    } catch (error) {
      console.error('Error applying strategy:', error);
      alert('Failed to apply strategy');
    }
    setProcessingColumn(false);
  };

  const groupedColumns = columnsData ? {
    numerical: Object.entries(columnsData)
      .filter(([_, type]) => type === 'numerical')
      .map(([col]) => col),
    categorical: Object.entries(columnsData)
      .filter(([_, type]) => type === 'categorical')
      .map(([col]) => col),
  } : null;

  return (
    <div className="mt-8">
      <button
        onClick={fetchColumnsTypes}
        disabled={loading}
        className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 
                 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
      >
        {loading ? 'Loading...' : 'Perform EDA'}
      </button>

      {groupedColumns && (
        <div className="mt-6 space-y-6">
          {/* Numerical Columns */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Numerical Columns</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {groupedColumns.numerical.map((column) => (
                <div key={column} className="relative">
                  <button
                    onClick={() => setSelectedColumn(selectedColumn === column ? null : column)}
                    className="w-full text-left px-4 py-2 bg-gray-50 rounded-md hover:bg-gray-100
                             flex justify-between items-center"
                  >
                    <span>{column}</span>
                    {selectedColumn === column ? (
                      <ChevronUp className="h-4 w-4" />
                    ) : (
                      <ChevronDown className="h-4 w-4" />
                    )}
                  </button>
                  {selectedColumn === column && (
                    <div className="absolute z-10 mt-1 w-full bg-white rounded-md shadow-lg">
                      {numericalStrategies.map((strategy) => (
                        <button
                          key={strategy}
                          onClick={() => handleStrategyClick(column, strategy)}
                          disabled={processingColumn}
                          className="w-full text-left px-4 py-2 hover:bg-gray-50 first:rounded-t-md 
                                   last:rounded-b-md"
                        >
                          {strategy}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Categorical Columns */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Categorical Columns</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {groupedColumns.categorical.map((column) => (
                <div key={column} className="relative">
                  <button
                    onClick={() => setSelectedColumn(selectedColumn === column ? null : column)}
                    className="w-full text-left px-4 py-2 bg-gray-50 rounded-md hover:bg-gray-100
                             flex justify-between items-center"
                  >
                    <span>{column}</span>
                    {selectedColumn === column ? (
                      <ChevronUp className="h-4 w-4" />
                    ) : (
                      <ChevronDown className="h-4 w-4" />
                    )}
                  </button>
                  {selectedColumn === column && (
                    <div className="absolute z-10 mt-1 w-full bg-white rounded-md shadow-lg">
                      {categoricalStrategies.map((strategy) => (
                        <button
                          key={strategy}
                          onClick={() => handleStrategyClick(column, strategy)}
                          disabled={processingColumn}
                          className="w-full text-left px-4 py-2 hover:bg-gray-50 first:rounded-t-md 
                                   last:rounded-b-md"
                        >
                          {strategy}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default EDASection;