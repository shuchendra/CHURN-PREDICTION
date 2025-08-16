const SampleDataset = () => {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md mt-6">
      <h3 className="text-lg font-medium text-gray-900 mb-4">Sample Dataset Format</h3>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Customer ID</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tenure</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Satisfaction Score</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Complaints</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Churn</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            <tr>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">001</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">24</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">4.5</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">2</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">No</td>
            </tr>
            <tr>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">002</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">12</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">3.8</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">5</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">Yes</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default SampleDataset;