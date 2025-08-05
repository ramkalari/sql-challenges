"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";

interface Challenge {
  id: number;
  name: string;
  level: string;
  question: string;
  solved?: boolean;
  solved_at?: string;
  attempts?: number;
  schema_tables: Array<{
    table_name: string;
    columns: Array<{
      name: string;
      type: string;
      constraints: string[];
    }>;
  }>;
}

interface QueryResult {
  passed: boolean;
  result?: Array<Array<string | number>>;
  column_names?: string[];
  expected?: Array<Array<string | number>>;
  expected_column_names?: string[];
  error?: string;
  message?: string;
  next_challenge?: {
    id: number;
    name: string;
    level: string;
  };
}

interface ApiError {
  response?: {
    status: number;
    data?: {
      detail?: string;
    };
  };
}

export default function ChallengesPage() {
  const [challenges, setChallenges] = useState<Challenge[]>([]);
  const [selectedChallenge, setSelectedChallenge] = useState<Challenge | null>(null);
  const [query, setQuery] = useState("SELECT * FROM ...");
  const [result, setResult] = useState<QueryResult | null>(null);
  const [error, setError] = useState("");
  const [userEmail, setUserEmail] = useState("");
  const [progressStats, setProgressStats] = useState({ solved: 0, total: 0 });
  const router = useRouter();

  useEffect(() => {
    // Check if user is authenticated
    const token = localStorage.getItem("token");
    const email = localStorage.getItem("userEmail");
    
    if (!token || !email) {
      router.push("/landing");
      return;
    }

    setUserEmail(email);
    
    // Set up axios defaults for authenticated requests
    axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
    
    const fetchChallenges = async () => {
      try {
        const res = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/challenges`);
        setChallenges(res.data);
        
        // Calculate progress stats
        const solved = res.data.filter((c: Challenge) => c.solved).length;
        setProgressStats({ solved, total: res.data.length });
      } catch (err: unknown) {
        const error = err as ApiError;
        if (error.response?.status === 401) {
          // Token expired or invalid
          localStorage.removeItem("token");
          localStorage.removeItem("userEmail");
          router.push("/landing");
        } else {
          setError("Failed to load challenges.");
        }
      }
    };
    fetchChallenges();
  }, [router]);

  const handleSelectChallenge = async (id: number) => {
    try {
      const res = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/challenges/${id}`);
      setSelectedChallenge(res.data);
      setQuery("");
      setResult(null);
      setError("");
    } catch (err: unknown) {
      const error = err as ApiError;
      if (error.response?.status === 401) {
        localStorage.removeItem("token");
        localStorage.removeItem("userEmail");
        router.push("/landing");
      } else {
        setError("Failed to load challenge details.");
      }
    }
  };

  const handleSubmit = async () => {
    if (!selectedChallenge) return;

    try {
      setError("");
      const res = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/challenges/${selectedChallenge.id}/submit`, {
        user_query: query,
      });
      setResult(res.data);
      
      // Update the challenges list immediately after successful submission
      if (res.data.passed) {
        setChallenges(prevChallenges => 
          prevChallenges.map(challenge => 
            challenge.id === selectedChallenge.id 
              ? { 
                  ...challenge, 
                  solved: true, 
                  solved_at: new Date().toISOString(),
                  attempts: (challenge.attempts || 0) + 1
                }
              : challenge
          )
        );
        
        // Update progress stats
        setProgressStats(prev => ({
          solved: prev.solved + 1,
          total: prev.total
        }));
      } else {
        // Update attempts count even for failed submissions
        setChallenges(prevChallenges => 
          prevChallenges.map(challenge => 
            challenge.id === selectedChallenge.id 
              ? { 
                  ...challenge, 
                  attempts: (challenge.attempts || 0) + 1
                }
              : challenge
          )
        );
      }
    } catch (err: unknown) {
      const error = err as ApiError;
      if (error.response?.status === 401) {
        localStorage.removeItem("token");
        localStorage.removeItem("userEmail");
        router.push("/landing");
      } else {
        setError(error.response?.data?.detail || "Error occurred");
      }
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("userEmail");
    router.push("/landing");
  };

  const handleNextChallenge = async () => {
    try {
      const res = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/challenges/next`);
      if (res.data.next_challenge) {
        handleSelectChallenge(res.data.next_challenge.id);
      }
    } catch (err: unknown) {
      const error = err as ApiError;
      if (error.response?.status === 401) {
        localStorage.removeItem("token");
        localStorage.removeItem("userEmail");
        router.push("/landing");
      } else {
        setError("Failed to get next challenge.");
      }
    }
  };

  const renderSchemaTable = (schemaTables: Challenge['schema_tables']) => {
    return (
      <div className="space-y-4">
        {schemaTables.map((table, tableIndex) => (
          <div key={tableIndex} className="bg-white border rounded-lg overflow-hidden">
            <div className="bg-gray-50 px-3 sm:px-4 py-2 border-b">
              <h4 className="font-semibold text-gray-800 text-sm sm:text-base">Table: {table.table_name}</h4>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full min-w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-3 sm:px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Column</th>
                    <th className="px-3 sm:px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                    <th className="px-3 sm:px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Constraints</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {table.columns.map((column, columnIndex) => (
                    <tr key={columnIndex}>
                      <td className="px-3 sm:px-4 py-2 whitespace-nowrap text-sm font-medium text-gray-900">{column.name}</td>
                      <td className="px-3 sm:px-4 py-2 whitespace-nowrap text-sm text-gray-500">{column.type}</td>
                      <td className="px-3 sm:px-4 py-2 whitespace-nowrap text-sm text-gray-500">
                        {column.constraints.length > 0 ? column.constraints.join(", ") : "None"}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        ))}
      </div>
    );
  };

  const renderResultTable = (data: Array<Array<string | number>>, title: string, columnNames?: string[]) => {
    if (!data || data.length === 0) return null;

    const headers = columnNames || Object.keys(data[0] || {});
    
    return (
      <div className="bg-white border rounded-lg overflow-hidden">
        <div className="bg-gray-50 px-3 sm:px-4 py-2 border-b">
          <h4 className="font-semibold text-gray-800 text-sm sm:text-base">{title}</h4>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full min-w-full">
            <thead className="bg-gray-50">
              <tr>
                {headers.map((header, index) => (
                  <th key={index} className="px-3 sm:px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    {header}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {data.map((row, rowIndex) => (
                <tr key={rowIndex}>
                  {row.map((cell, cellIndex) => (
                    <td key={cellIndex} className="px-3 sm:px-4 py-2 whitespace-nowrap text-sm text-gray-900">
                      {String(cell)}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-gray-900">SQL Challenges</h1>
            </div>
            <div className="flex flex-col sm:flex-row items-start sm:items-center space-y-2 sm:space-y-0 sm:space-x-4">
              <div className="flex items-center space-x-3">
                <div className="text-sm text-gray-600">
                  <span className="font-medium">{progressStats.solved}</span> of <span className="font-medium">{progressStats.total}</span> solved
                </div>
                <div className="w-20 sm:w-24 bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-green-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${progressStats.total > 0 ? (progressStats.solved / progressStats.total) * 100 : 0}%` }}
                  ></div>
                </div>
              </div>
              <div className="flex items-center space-x-2 sm:space-x-4">
                <span className="text-sm text-gray-600 hidden sm:block">Welcome, {userEmail}</span>
                <button
                  onClick={() => router.push("/profile")}
                  className="px-3 sm:px-4 py-2 text-sm font-medium text-blue-600 hover:text-blue-700"
                >
                  Profile
                </button>
                <button
                  onClick={handleLogout}
                  className="px-3 sm:px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900"
                >
                  Logout
                </button>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-8">
        <div className="flex flex-col lg:flex-row h-[calc(100vh-200px)]">
          {/* Sidebar */}
          <div className="w-full lg:w-1/4 lg:pr-8 mb-6 lg:mb-0 lg:overflow-y-auto">
            <h2 className="text-xl font-bold mb-4 sticky top-0 bg-gray-50 py-2">Challenges</h2>
            <div className="space-y-2">
              {challenges.map((c) => (
                <button
                  key={c.id}
                  onClick={() => handleSelectChallenge(c.id)}
                  className={`w-full text-left p-3 rounded-lg border transition-colors ${
                    selectedChallenge?.id === c.id
                      ? "bg-blue-50 border-blue-200 text-blue-900"
                      : "bg-white border-gray-200 hover:bg-gray-50"
                  }`}
                >
                  <div className="flex justify-between items-center">
                    <div className="flex items-center space-x-2">
                      <span className="font-medium">{c.name}</span>
                      {c.solved && (
                        <svg className="w-4 h-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                        </svg>
                      )}
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className={`text-xs px-2 py-1 rounded-full ${
                        c.level === 'Basic' ? 'bg-green-100 text-green-800' :
                        c.level === 'Intermediate' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {c.level}
                      </span>
                      {c.attempts && c.attempts > 0 && (
                        <span className="text-xs text-gray-500">
                          {c.attempts} {c.attempts === 1 ? 'attempt' : 'attempts'}
                        </span>
                      )}
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Main Content */}
          <div className="w-full lg:w-3/4 lg:overflow-y-auto">
            {selectedChallenge ? (
              <div className="bg-white rounded-lg shadow-sm border p-4 sm:p-6">
                <div className="mb-4 sm:mb-6">
                  <h1 className="text-xl sm:text-2xl font-bold text-gray-900 mb-2">{selectedChallenge.name}</h1>
                  <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${
                    selectedChallenge.level === 'Basic' ? 'bg-green-100 text-green-800' :
                    selectedChallenge.level === 'Intermediate' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
                  }`}>
                    {selectedChallenge.level}
                  </span>
                </div>
                
                <div className="mb-4 sm:mb-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">Question</h3>
                  <p className="text-gray-700 bg-gray-50 p-3 sm:p-4 rounded-lg text-sm sm:text-base">{selectedChallenge.question}</p>
                </div>

                <div className="mb-4 sm:mb-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">Database Schema</h3>
                  <div className="overflow-x-auto">
                    {renderSchemaTable(selectedChallenge.schema_tables)}
                  </div>
                </div>

                <div className="mb-4 sm:mb-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">Your Query</h3>
                  <textarea
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    className="w-full h-24 sm:h-32 border border-gray-300 rounded-lg p-3 font-mono text-sm text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Write your SQL query here..."
                  />
                </div>

                <button
                  onClick={handleSubmit}
                  className="w-full sm:w-auto bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors duration-200"
                >
                  Run Query
                </button>

                {error && (
                  <div className="mt-4 bg-red-50 border border-red-200 rounded-lg p-4">
                    <p className="text-red-600 text-sm">{error}</p>
                  </div>
                )}

                {result && (
                  <div className="mt-6">
                    <div className="mb-4 flex items-center justify-between">
                      <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                        result.passed 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-red-100 text-red-800'
                      }`}>
                        {result.passed ? "✅ Passed" : "❌ Failed"}
                      </span>
                      
                                             {result.passed && result.next_challenge && (
                         <button
                           onClick={handleNextChallenge}
                           className="inline-flex items-center px-4 py-2 bg-green-600 text-white text-sm font-medium rounded-lg hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-colors duration-200"
                         >
                           Next Challenge →
                         </button>
                       )}
                    </div>
                    
                    <div className="grid grid-cols-1 gap-4 sm:gap-6">
                      {renderResultTable(result.result || [], "Your Result", result.column_names)}
                      {!result.passed && renderResultTable(result.expected || [], "Expected Result", result.expected_column_names)}
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="bg-white rounded-lg shadow-sm border p-8 sm:p-12 text-center">
                <div className="max-w-md mx-auto">
                  <svg className="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <h3 className="text-lg font-medium text-gray-900 mb-2">Select a Challenge</h3>
                  <p className="text-gray-500 text-sm sm:text-base">Choose a challenge from the sidebar to start practicing SQL queries.</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
} 