import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import LoadingSpinner from '../components/LoadingSpinner';
import { ChevronDown, ChevronUp } from 'lucide-react';
import { useUpload } from '../context/UploadContext';

const Questions = () => {
  const [questions, setQuestions] = useState([]);
  const [visualizations, setVisualizations] = useState({});
  const [expandedQuestion, setExpandedQuestion] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const [loadingVisualizations, setLoadingVisualizations] = useState({});
  const { filesUploaded } = useUpload();
  const navigate = useNavigate();

  useEffect(() => {
    if (!filesUploaded) {
      navigate('/');
      return;
    }

    const fetchQuestions = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/documentation/generate-questions');
        if (response.ok) {
          const data = await response.json();
          setQuestions(data.questions);
        } else {
          setError('Failed to fetch questions');
        }
      } catch (err) {
        setError('Network error while fetching questions');
      } finally {
        setLoading(false);
      }
    };

    fetchQuestions();
  }, [filesUploaded, navigate]);

  const fetchVisualizations = async (questionNumber) => {
    setLoadingVisualizations(prev => ({ ...prev, [questionNumber]: true }));
    try {
      const response = await fetch(`http://127.0.0.1:8000/create-visualization/${questionNumber}`);
      if (response.ok) {
        const data = await response.json();
        setVisualizations({ ...visualizations, [questionNumber]: data.visualizations });
      } else {
        setError('Failed to fetch visualizations');
      }
    } catch (err) {
      setError('Network error while fetching visualizations');
    } finally {
      setLoadingVisualizations(prev => ({ ...prev, [questionNumber]: false }));
    }
  };

  const handleQuestionClick = async (questionNumber) => {
    if (expandedQuestion === questionNumber) {
      setExpandedQuestion(null);
    } else {
      setExpandedQuestion(questionNumber);
      if (!visualizations[questionNumber]) {
        await fetchVisualizations(questionNumber);
      }
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      
      <main className="flex-grow container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold text-gray-900 mb-6">Business Questions Analysis</h1>
          
          {error && (
            <div className="bg-red-50 p-4 rounded-md mb-6">
              <p className="text-red-700">{error}</p>
            </div>
          )}

          {loading ? (
            <LoadingSpinner />
          ) : (
            <div className="space-y-4">
              {questions.map((question, index) => (
                <div key={index} className="bg-white rounded-lg shadow-md overflow-hidden">
                  <button
                    onClick={() => handleQuestionClick(question.split(')')[0] + ')')}
                    className="w-full text-left p-4 flex justify-between items-center hover:bg-gray-50"
                  >
                    <span className="font-medium">{question}</span>
                    {expandedQuestion === (question.split(')')[0] + ')') ? (
                      <ChevronUp className="h-5 w-5 text-gray-500" />
                    ) : (
                      <ChevronDown className="h-5 w-5 text-gray-500" />
                    )}
                  </button>

                  {expandedQuestion === (question.split(')')[0] + ')') && (
                    <div className="p-4 border-t">
                      {loadingVisualizations[question.split(')')[0] + ')'] ? (
                        <LoadingSpinner />
                      ) : visualizations[question.split(')')[0] + ')'] && (
                        Object.entries(visualizations[question.split(')')[0] + ')']).map(([key, value]) => (
                          <div key={key} className="mb-6">
                            <h3 className="text-lg font-medium text-gray-900 mb-4">{key}</h3>
                            {Array.isArray(value) ? (
                              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                {value.map((image, i) => (
                                  <img
                                    key={i}
                                    src={`http://127.0.0.1:8000/graphs/${image}`}
                                    alt={`Visualization ${i + 1}`}
                                    className="w-full rounded-lg shadow-md"
                                  />
                                ))}
                              </div>
                            ) : key === 'relationship' ? (
                              Object.entries(value).map(([chartType, chartData]) => (
                                <div key={chartType} className="mb-6">
                                  <h4 className="text-md font-medium text-gray-800 mb-2">{chartType}</h4>
                                  <img
                                    src={`http://127.0.0.1:8000/graphs/${chartData.image}`}
                                    alt={chartType}
                                    className="w-full rounded-lg shadow-md mb-4"
                                  />
                                  <div className="bg-gray-50 p-4 rounded-md">
                                    <p className="font-medium text-gray-900 mb-2">
                                      Relationship Analysis: {chartData.relationship_analysis.relationships_analysis}
                                    </p>
                                    <p className="text-gray-600">
                                      {chartData.relationship_analysis.explanation}
                                    </p>
                                  </div>
                                </div>
                              ))
                            ) : null}
                          </div>
                        ))
                      )}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Questions