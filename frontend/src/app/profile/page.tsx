"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";

interface ProgressItem {
  challenge_id: number;
  challenge_name: string;
  level: string;
  solved_at: string;
  attempts: number;
}

interface SubmissionItem {
  challenge_id: number;
  challenge_name: string;
  query: string;
  passed: boolean;
  submitted_at: string;
}

interface ApiError {
  response?: {
    status: number;
  };
}

export default function ProfilePage() {
  const [userEmail, setUserEmail] = useState("");
  const [progress, setProgress] = useState<ProgressItem[]>([]);
  const [submissions, setSubmissions] = useState<SubmissionItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
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
    
    const fetchData = async () => {
      try {
        const [progressRes, submissionsRes] = await Promise.all([
          axios.get(`${process.env.NEXT_PUBLIC_API_URL}/user/progress`),
          axios.get(`${process.env.NEXT_PUBLIC_API_URL}/user/submissions`)
        ]);
        
        setProgress(progressRes.data.progress);
        setSubmissions(submissionsRes.data.submissions);
      } catch (err: unknown) {
        const error = err as ApiError;
        if (error.response?.status === 401) {
          localStorage.removeItem("token");
          localStorage.removeItem("userEmail");
          router.push("/landing");
        } else {
          setError("Failed to load profile data.");
        }
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("userEmail");
    router.push("/landing");
  };

  const handleBackToChallenges = () => {
    router.push("/challenges");
  };

  const getLevelColor = (level: string) => {
    switch (level) {
      case 'Basic': return 'bg-green-100 text-green-800';
      case 'Intermediate': return 'bg-yellow-100 text-yellow-800';
      case 'Advanced': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const totalSubmissions = submissions.length;
  const successfulSubmissions = submissions.filter(s => s.passed).length;
  const successRate = totalSubmissions > 0 ? (successfulSubmissions / totalSubmissions * 100).toFixed(1) : '0';

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading profile...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex flex-col sm:flex-row items-start sm:items-center space-y-2 sm:space-y-0 sm:space-x-4">
              <div className="flex items-center space-x-4">
                <button
                  onClick={handleBackToChallenges}
                  className="text-blue-600 hover:text-blue-700 font-medium text-sm sm:text-base"
                >
                  ← Back to Challenges
                </button>
                <h1 className="text-xl font-bold text-gray-900">Profile</h1>
              </div>
            </div>
            <div className="flex items-center space-x-2 sm:space-x-4">
              <span className="text-sm text-gray-600 hidden sm:block">Welcome, {userEmail}</span>
              <button
                onClick={handleLogout}
                className="px-3 sm:px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
            <p className="text-red-600">{error}</p>
          </div>
        )}

        {/* Stats Overview */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6 mb-6 sm:mb-8">
          <div className="bg-white rounded-lg shadow-sm border p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <svg className="w-8 h-8 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Challenges Solved</p>
                <p className="text-2xl font-bold text-gray-900">{progress.length}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <svg className="w-8 h-8 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Total Submissions</p>
                <p className="text-2xl font-bold text-gray-900">{totalSubmissions}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <svg className="w-8 h-8 text-yellow-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Success Rate</p>
                <p className="text-2xl font-bold text-gray-900">{successRate}%</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <svg className="w-8 h-8 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 13v1a2 2 0 01-2 2H5a2 2 0 01-2-2v-1a5 5 0 0110 0c0 .34.024.673.07 1H12.93z" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Account Created</p>
                <p className="text-sm font-bold text-gray-900">Active</p>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 sm:gap-8">
          {/* Solved Challenges */}
          <div className="bg-white rounded-lg shadow-sm border">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-900">Solved Challenges</h2>
            </div>
            <div className="p-6">
              {progress.length === 0 ? (
                <div className="text-center py-8">
                  <svg className="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <p className="text-gray-500">No challenges solved yet. Start practicing!</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {progress.map((item) => (
                    <div key={item.challenge_id} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex justify-between items-start">
                        <div>
                          <h3 className="font-medium text-gray-900">{item.challenge_name}</h3>
                          <p className="text-sm text-gray-500 mt-1">
                            Solved on {formatDate(item.solved_at)}
                          </p>
                        </div>
                        <div className="flex items-center space-x-2">
                          <span className={`text-xs px-2 py-1 rounded-full ${getLevelColor(item.level)}`}>
                            {item.level}
                          </span>
                          <span className="text-xs text-gray-500">
                            {item.attempts} {item.attempts === 1 ? 'attempt' : 'attempts'}
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Recent Submissions */}
          <div className="bg-white rounded-lg shadow-sm border">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-900">Recent Submissions</h2>
            </div>
            <div className="p-6">
              {submissions.length === 0 ? (
                <div className="text-center py-8">
                  <svg className="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                  </svg>
                  <p className="text-gray-500">No submissions yet. Start solving challenges!</p>
                </div>
              ) : (
                                 <div className="space-y-4 max-h-96 overflow-y-auto">
                   {submissions.slice(0, 10).map((submission, index) => (
                     <div key={index} className="border border-gray-200 rounded-lg p-3 sm:p-4">
                       <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start mb-2 space-y-2 sm:space-y-0">
                         <h3 className="font-medium text-gray-900 text-sm sm:text-base">{submission.challenge_name}</h3>
                         <div className="flex items-center space-x-2">
                           <span className={`text-xs px-2 py-1 rounded-full ${
                             submission.passed ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                           }`}>
                             {submission.passed ? 'Passed' : 'Failed'}
                           </span>
                           <span className="text-xs text-gray-500">
                             {formatDate(submission.submitted_at)}
                           </span>
                         </div>
                       </div>
                       <div className="bg-gray-50 rounded p-2 sm:p-3">
                         <p className="text-xs sm:text-sm font-mono text-gray-700 break-all">
                           {submission.query}
                         </p>
                       </div>
                     </div>
                   ))}
                 </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 