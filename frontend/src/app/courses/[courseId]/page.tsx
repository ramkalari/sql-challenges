"use client";
import { useState, useEffect, useRef } from "react";
import { useRouter, useParams } from "next/navigation";
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

interface Course {
  id: string;
  name: string;
  description: string;
  icon: string;
  difficulty: string;
  duration: string;
  features: string[];
  technologies: string[];
  is_available: boolean;
  progress: {
    solved: number;
    total: number;
    percentage: number;
  };
}

interface QueryResult {
  passed: boolean;
  result: string[][];
  expected: string[][];
  column_names: string[];
  expected_column_names: string[];
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

export default function CoursePage() {
  const [course, setCourse] = useState<Course | null>(null);
  const [challenges, setChallenges] = useState<Challenge[]>([]);
  const [selectedChallenge, setSelectedChallenge] = useState<Challenge | null>(null);
  const [query, setQuery] = useState("SELECT * FROM ...");
  const [result, setResult] = useState<QueryResult | null>(null);
  const [error, setError] = useState("");
  const [userEmail, setUserEmail] = useState("");
  const [databaseType, setDatabaseType] = useState("sqlite");
  const router = useRouter();
  const params = useParams();
  const courseId = params.courseId as string;
  const resultsRef = useRef<HTMLDivElement>(null);

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
    
    const fetchData = async () => {
      try {
        const [courseRes, challengesRes] = await Promise.all([
          axios.get(`${process.env.NEXT_PUBLIC_API_URL}/courses/${courseId}`),
          axios.get(`${process.env.NEXT_PUBLIC_API_URL}/courses/${courseId}/challenges`)
        ]);
        
        setCourse(courseRes.data);
        setChallenges(challengesRes.data.challenges);
      } catch (err: unknown) {
        const error = err as ApiError;
        if (error.response?.status === 401) {
          // Token expired or invalid
          localStorage.removeItem("token");
          localStorage.removeItem("userEmail");
          router.push("/landing");
        } else if (error.response?.status === 404) {
          setError("Course not found.");
        } else {
          setError("Failed to load course data.");
        }
      }
    };
    
    fetchData();
  }, [router, courseId]);

  // Auto-scroll to results/error section when they appear
  useEffect(() => {
    if (result || error) {
      resultsRef.current?.scrollIntoView({ 
        behavior: 'smooth', 
        block: 'start' 
      });
    }
  }, [result, error]);

  const handleSelectChallenge = async (id: number) => {
    try {
      const res = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/challenges/${id}`);
      setSelectedChallenge(res.data);
      setResult(null);
      setError("");
      
      // Update the local challenges state to reflect any progress changes
      setChallenges(prev => prev.map(c => 
        c.id === id ? { ...c, solved: res.data.solved, attempts: res.data.attempts } : c
      ));
    } catch (err: unknown) {
      setError("Failed to load challenge details.");
    }
  };

  const handleSubmit = async () => {
    if (!selectedChallenge) return;
    
    setError("");
    setResult(null);
    
    try {
      const res = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/challenges/${selectedChallenge.id}/submit`,
        {
          user_query: query,
          database_type: databaseType
        }
      );
      
      const data: QueryResult = res.data;
      setResult(data);
      
      // Update challenge status in the sidebar
      setChallenges(prev => prev.map(c => 
        c.id === selectedChallenge.id 
          ? { ...c, solved: data.passed, attempts: (c.attempts || 0) + 1 }
          : c
      ));

      // Update course progress
      if (course && data.passed) {
        setCourse(prev => prev ? {
          ...prev,
          progress: {
            ...prev.progress,
            solved: prev.progress.solved + 1,
            percentage: ((prev.progress.solved + 1) / prev.progress.total * 100)
          }
        } : null);
      }
      
    } catch (err: unknown) {
      const error = err as ApiError;
      setError(error.response?.data?.detail || "Failed to execute query");
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("userEmail");
    router.push("/landing");
  };

  const handleBackToHome = () => {
    router.push("/");
  };

  const handleProfile = () => {
    router.push("/profile");
  };

  const getLevelColor = (level: string) => {
    switch (level) {
      case "Basic": return "bg-green-100 text-green-800";
      case "Intermediate": return "bg-yellow-100 text-yellow-800";
      case "Advanced": return "bg-red-100 text-red-800";
      default: return "bg-gray-100 text-gray-800";
    }
  };

  if (!course) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading course...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center space-x-4">
              <button
                onClick={handleBackToHome}
                className="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
              >
                ← All Courses
              </button>
              <div className="h-6 border-l border-gray-300"></div>
              <div className="flex items-center">
                <span className="text-2xl mr-3">{course.icon}</span>
                <h1 className="text-xl font-bold text-gray-900">{course.name}</h1>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">Welcome, {userEmail}</span>
              <button
                onClick={handleProfile}
                className="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
              >
                Profile
              </button>
              <button
                onClick={handleLogout}
                className="bg-red-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-red-700"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex flex-col lg:flex-row gap-6">
          {/* Sidebar */}
          <div className="w-full lg:w-80 bg-white rounded-lg shadow-sm p-6">
            {/* Course Progress */}
            <div className="mb-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-3">Course Progress</h2>
              <div className="bg-gray-200 rounded-full h-2 mb-2">
                <div 
                  className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${course.progress.percentage}%` }}
                ></div>
              </div>
              <p className="text-sm text-gray-600">
                {course.progress.solved} of {course.progress.total} challenges completed ({course.progress.percentage}%)
              </p>
            </div>

            {/* Challenges List */}
            <div>
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Challenges</h2>
              <div className="space-y-2">
                {challenges.map((challenge) => (
                  <button
                    key={challenge.id}
                    onClick={() => handleSelectChallenge(challenge.id)}
                    className={`w-full text-left p-3 rounded-lg border transition-all duration-200 ${
                      selectedChallenge?.id === challenge.id
                        ? "border-blue-500 bg-blue-50"
                        : "border-gray-200 hover:border-gray-300 hover:bg-gray-50"
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="font-medium text-gray-900">{challenge.name}</span>
                      {challenge.solved && (
                        <span className="text-green-500 text-sm">✓</span>
                      )}
                    </div>
                    <div className="flex items-center justify-between">
                      <span className={`inline-block px-2 py-1 rounded-full text-xs font-medium ${getLevelColor(challenge.level)}`}>
                        {challenge.level}
                      </span>
                      {challenge.attempts > 0 && (
                        <span className="text-xs text-gray-500">
                          {challenge.attempts} attempt{challenge.attempts !== 1 ? 's' : ''}
                        </span>
                      )}
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Main Content */}
          <div className="flex-1 bg-white rounded-lg shadow-sm p-6">
            {selectedChallenge ? (
              <>
                <div className="mb-6">
                  <div className="flex items-center justify-between mb-4">
                    <h2 className="text-2xl font-bold text-gray-900">{selectedChallenge.name}</h2>
                    <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${getLevelColor(selectedChallenge.level)}`}>
                      {selectedChallenge.level}
                    </span>
                  </div>
                  
                  <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                    <h3 className="text-lg font-semibold text-blue-900 mb-2">Question</h3>
                    <p className="text-blue-800">{selectedChallenge.question}</p>
                  </div>

                  {/* Schema Display */}
                  <div className="mb-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-3">Database Schema</h3>
                    <div className="space-y-4">
                      {selectedChallenge.schema_tables.map((table, index) => (
                        <div key={index} className="border border-gray-200 rounded-lg overflow-hidden">
                          <div className="bg-gray-50 px-4 py-2 border-b border-gray-200">
                            <h4 className="font-semibold text-gray-900">Table: {table.table_name}</h4>
                          </div>
                          <div className="overflow-x-auto">
                            <table className="min-w-full divide-y divide-gray-200">
                              <thead className="bg-gray-50">
                                <tr>
                                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Column</th>
                                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Constraints</th>
                                </tr>
                              </thead>
                              <tbody className="bg-white divide-y divide-gray-200">
                                {table.columns.map((column, colIndex) => (
                                  <tr key={colIndex}>
                                    <td className="px-4 py-2 text-sm font-medium text-gray-900">{column.name}</td>
                                    <td className="px-4 py-2 text-sm text-gray-500">{column.type}</td>
                                    <td className="px-4 py-2 text-sm text-gray-500">{column.constraints.join(", ") || "-"}</td>
                                  </tr>
                                ))}
                              </tbody>
                            </table>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="mb-4 sm:mb-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">Database Engine</h3>
                  <select
                    value={databaseType}
                    onChange={(e) => setDatabaseType(e.target.value)}
                    className="w-full sm:w-auto border border-gray-300 rounded-lg p-3 text-sm text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white"
                  >
                    <option value="sqlite">SQLite</option>
                    <option value="duckdb">DuckDB</option>
                  </select>
                  <p className="mt-2 text-sm text-gray-600">
                    Choose between SQLite (traditional relational) or DuckDB (analytical) database engines.
                  </p>
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

                <div ref={resultsRef}>
                  {error && (
                    <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                      <h3 className="text-lg font-semibold text-red-900 mb-2">Error</h3>
                      <p className="text-red-800">{error}</p>
                    </div>
                  )}

                  {result && (
                    <div className="mt-6 space-y-6">
                      {result.passed ? (
                        <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                          <h3 className="text-lg font-semibold text-green-900 mb-2">✅ Correct!</h3>
                          <p className="text-green-800">Great job! Your query returned the expected results.</p>
                          {result.next_challenge && (
                            <div className="mt-3">
                              <p className="text-green-700">
                                Next challenge: <strong>{result.next_challenge.name}</strong> ({result.next_challenge.level})
                              </p>
                              <button
                                onClick={() => handleSelectChallenge(result.next_challenge!.id)}
                                className="mt-2 bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 text-sm"
                              >
                                Go to Next Challenge
                              </button>
                            </div>
                          )}
                        </div>
                      ) : (
                        <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                          <h3 className="text-lg font-semibold text-yellow-900 mb-2">❌ Not quite right</h3>
                          <p className="text-yellow-800">Your query ran successfully, but the results don't match what's expected. Try again!</p>
                        </div>
                      )}

                      {/* Results comparison */}
                      <div className="grid gap-6 md:grid-cols-2">
                        <div>
                          <h4 className="text-md font-semibold text-gray-900 mb-2">Your Results</h4>
                          <div className="border border-gray-200 rounded-lg overflow-hidden">
                            <table className="min-w-full divide-y divide-gray-200">
                              <thead className="bg-gray-50">
                                <tr>
                                  {result.column_names.map((col, index) => (
                                    <th key={index} className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                      {col}
                                    </th>
                                  ))}
                                </tr>
                              </thead>
                              <tbody className="bg-white divide-y divide-gray-200">
                                {result.result.map((row, rowIndex) => (
                                  <tr key={rowIndex}>
                                    {row.map((cell, cellIndex) => (
                                      <td key={cellIndex} className="px-4 py-2 text-sm text-gray-900">
                                        {cell}
                                      </td>
                                    ))}
                                  </tr>
                                ))}
                              </tbody>
                            </table>
                          </div>
                        </div>

                        <div>
                          <h4 className="text-md font-semibold text-gray-900 mb-2">Expected Results</h4>
                          <div className="border border-gray-200 rounded-lg overflow-hidden">
                            <table className="min-w-full divide-y divide-gray-200">
                              <thead className="bg-gray-50">
                                <tr>
                                  {result.expected_column_names.map((col, index) => (
                                    <th key={index} className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                      {col}
                                    </th>
                                  ))}
                                </tr>
                              </thead>
                              <tbody className="bg-white divide-y divide-gray-200">
                                {result.expected.map((row, rowIndex) => (
                                  <tr key={rowIndex}>
                                    {row.map((cell, cellIndex) => (
                                      <td key={cellIndex} className="px-4 py-2 text-sm text-gray-900">
                                        {cell}
                                      </td>
                                    ))}
                                  </tr>
                                ))}
                              </tbody>
                            </table>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </>
            ) : (
              <div className="text-center py-12">
                <div className="text-6xl mb-4">🎯</div>
                <h2 className="text-2xl font-bold text-gray-900 mb-2">Select a Challenge</h2>
                <p className="text-gray-600">Choose a challenge from the sidebar to start practicing SQL queries.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
} 