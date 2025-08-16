import { BarChart2 } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';

const Navbar = () => {
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path ? 'text-white' : 'text-indigo-200 hover:text-white';
  };

  return (
    <nav className="bg-indigo-600 text-white p-4">
      <div className="container mx-auto flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <BarChart2 className="h-6 w-6" />
          <span className="text-xl font-bold">Churn Predictor</span>
        </div>
        <div className="flex items-center space-x-6">
          <Link to="/" className={`${isActive('/')} transition-colors duration-200`}>
            Home
          </Link>
          <Link to="/dataset-info" className={`${isActive('/dataset-info')} transition-colors duration-200`}>
            Dataset Info
          </Link>
          <Link to="/questions" className={`${isActive('/questions')} transition-colors duration-200`}>
            Analysis
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;