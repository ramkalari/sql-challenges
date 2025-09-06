'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';

interface LeaderboardEntry {
  rank: number;
  email: string;
  total_score: number;
  challenges_solved: number;
  total_attempts: number;
  efficiency_rate: number;
  last_solved: string;
}

interface ApiError {
  response?: {
    status: number;
    data?: {
      detail?: string;
    };
  };
}

export default function LeaderboardPage() {
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [userEmail, setUserEmail] = useState("");
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
    
    const fetchLeaderboard = async () => {
      try {
        const res = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/leaderboard`);
        setLeaderboard(res.data.leaderboard);
      } catch (err: unknown) {
        const error = err as ApiError;
        if (error.response?.status === 401) {
          localStorage.removeItem("token");
          localStorage.removeItem("userEmail");
          router.push("/landing");
        } else {
          setError("Failed to load leaderboard data.");
        }
      } finally {
        setLoading(false);
      }
    };
    
    fetchLeaderboard();
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("userEmail");
    router.push("/landing");
  };

  const handleBackToHome = () => {
    router.push("/");
  };

  const getRankColor = (rank: number) => {
    if (rank === 1) return "text-yellow-600"; // Gold
    if (rank === 2) return "text-gray-600"; // Silver
    if (rank === 3) return "text-amber-600"; // Bronze
    return "text-gray-800";
  };

  const getRankIcon = (rank: number) => {
    if (rank === 1) return "🏆";
    if (rank === 2) return "🥈";
    if (rank === 3) return "🥉";
    return `#${rank}`;
  };

  const formatDate = (dateString: string) => {
    if (!dateString) return "Never";
    return new Date(dateString).toLocaleDateString();
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading leaderboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-4">
              <h1 className="text-2xl font-bold text-gray-900">Brickwall Academy</h1>
              <span className="text-sm text-gray-500">Leaderboard</span>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">Welcome, {userEmail}</span>
              <button
                                  onClick={handleBackToHome}
                className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
              >
                Challenges
              </button>
              <button
                onClick={handleLogout}
                className="bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700 transition-colors"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">🏆 Top Performers</h2>
            <p className="text-sm text-gray-600 mt-1">
              Ranked by total score (based on challenge difficulty and efficiency)
            </p>
          </div>

          {leaderboard.length === 0 ? (
            <div className="px-6 py-8 text-center text-gray-500">
              <p className="text-lg">No one has solved any challenges yet!</p>
              <p className="text-sm mt-2">Be the first to make it on the leaderboard.</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Rank
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      User
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Score
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Challenges Solved
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Efficiency Rate
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Last Solved
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {leaderboard.map((entry) => (
                    <tr 
                      key={entry.rank}
                      className={`${
                        entry.email === userEmail ? 'bg-blue-50 border-l-4 border-blue-500' : 'hover:bg-gray-50'
                      }`}
                    >
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className={`text-lg font-bold ${getRankColor(entry.rank)}`}>
                          {getRankIcon(entry.rank)}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          <div className="text-sm font-medium text-gray-900">
                            {entry.email}
                            {entry.email === userEmail && (
                              <span className="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                                You
                              </span>
                            )}
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-bold text-gray-900">
                          {entry.total_score} pts
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900">
                          {entry.challenges_solved}
                        </div>
                        <div className="text-xs text-gray-500">
                          {entry.total_attempts} attempts
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900">
                          {entry.efficiency_rate}%
                        </div>
                        <div className="w-16 bg-gray-200 rounded-full h-1.5 mt-1">
                          <div 
                            className="bg-green-500 h-1.5 rounded-full" 
                            style={{width: `${Math.min(entry.efficiency_rate, 100)}%`}}
                          ></div>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {formatDate(entry.last_solved)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* Scoring Information */}
        <div className="mt-8 bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">How Scoring Works</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">Basic</div>
              <div className="text-sm text-gray-600">10 points</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-yellow-600">Intermediate</div>
              <div className="text-sm text-gray-600">20 points</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-red-600">Advanced</div>
              <div className="text-sm text-gray-600">30 points</div>
            </div>
          </div>
          <div className="mt-4 text-sm text-gray-600 text-center">
            <p><strong>Efficiency Bonus:</strong> Solve challenges in fewer attempts for up to 50% bonus points!</p>
            <p className="mt-1"><strong>Efficiency Rate:</strong> (Challenges Solved ÷ Total Attempts) × 100</p>
          </div>
        </div>
      </main>
    </div>
  );
} 