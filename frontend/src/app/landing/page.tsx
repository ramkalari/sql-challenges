"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";

interface AuthResponse {
  access_token: string;
  token_type: string;
  email: string;
}

interface ApiError {
  response?: {
    data?: {
      detail?: string;
    };
  };
}

export default function LandingPage() {
  const [isSignup, setIsSignup] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const endpoint = isSignup ? "/auth/signup" : "/auth/login";
      const res = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}${endpoint}`, {
        email,
        password,
      });

      const data: AuthResponse = res.data;
      
      // Store token and email
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("userEmail", data.email);
      
      // Redirect to challenges
      router.push("/challenges");
    } catch (err: unknown) {
      const error = err as ApiError;
      setError(error.response?.data?.detail || "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-gray-900">SQL Challenges</h1>
            </div>
            <div className="flex items-center space-x-2 sm:space-x-4">
              <button
                onClick={() => setIsSignup(false)}
                className={`px-3 sm:px-4 py-2 rounded-md text-sm font-medium transition-all duration-200 ${
                  !isSignup
                    ? "bg-blue-600 text-white shadow-md"
                    : "text-gray-700 hover:text-gray-900 hover:bg-gray-100"
                }`}
              >
                Login
              </button>
              <button
                onClick={() => setIsSignup(true)}
                className={`px-3 sm:px-4 py-2 rounded-md text-sm font-medium transition-all duration-200 ${
                  isSignup
                    ? "bg-blue-600 text-white shadow-md"
                    : "text-gray-700 hover:text-gray-900 hover:bg-gray-100"
                }`}
              >
                Sign Up
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content with Sidebar Layout */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
        <div className="flex flex-col lg:flex-row gap-8 lg:gap-12">
          {/* Main Content */}
          <div className="flex-1">
            <div className="text-center lg:text-left">
              <h1 className="text-3xl font-extrabold text-gray-900 sm:text-4xl md:text-5xl lg:text-6xl">
                Master SQL with
                <span className="text-blue-600"> Interactive Challenges</span>
              </h1>
              <p className="mt-3 max-w-md mx-auto lg:mx-0 text-sm text-gray-500 sm:text-base md:mt-5 md:text-lg lg:text-xl md:max-w-3xl px-4 lg:px-0">
                Practice SQL queries with real-world scenarios. Get instant feedback and improve your database skills.
              </p>
            </div>

            {/* Features */}
            <div className="mt-12 sm:mt-16">
              <div className="grid grid-cols-1 gap-6 sm:gap-8 sm:grid-cols-2 lg:grid-cols-3">
                <div className="bg-white rounded-lg shadow-md p-6">
                  <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                    <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <h3 className="text-lg font-medium text-gray-900 mb-2">Instant Feedback</h3>
                  <p className="text-gray-600">Get immediate results and see how your queries perform against expected outputs.</p>
                </div>

                <div className="bg-white rounded-lg shadow-md p-6">
                  <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
                    <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                    </svg>
                  </div>
                  <h3 className="text-lg font-medium text-gray-900 mb-2">Real Database Schema</h3>
                  <p className="text-gray-600">Practice with realistic table structures and data that you&apos;ll encounter in real projects.</p>
                </div>

                <div className="bg-white rounded-lg shadow-md p-6">
                  <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
                    <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                  </div>
                  <h3 className="text-lg font-medium text-gray-900 mb-2">Progressive Learning</h3>
                  <p className="text-gray-600">Start with basic queries and advance to complex joins, aggregations, and subqueries.</p>
                </div>
              </div>
            </div>
          </div>

          {/* Auth Form Sidebar */}
          <div className="lg:w-96 lg:flex-shrink-0">
            <div className="bg-white rounded-lg shadow-lg p-6 sm:p-8 relative overflow-hidden sticky top-8">
              {/* Smooth transition overlay */}
              <div className={`absolute inset-0 bg-blue-50 transform transition-transform duration-300 ease-in-out ${
                isSignup ? 'translate-x-0' : '-translate-x-full'
              }`}></div>
              
              <div className="relative z-10">
                <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center transition-all duration-300 transform">
                  {isSignup ? "Create Your Account" : "Welcome Back"}
                </h2>
              
              <form onSubmit={handleSubmit} className="space-y-6 transition-all duration-300">
                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                    Email Address
                  </label>
                  <input
                    id="email"
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Enter your email"
                  />
                </div>

                <div>
                  <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                    Password
                  </label>
                  <input
                    id="password"
                    type="password"
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Enter your password"
                  />
                  {!isSignup && (
                    <div className="mt-2 text-right">
                      <button
                        type="button"
                        onClick={() => router.push('/forgot-password')}
                        className="text-sm text-blue-600 hover:text-blue-500 font-medium transition-colors duration-200"
                      >
                        Forgot Password?
                      </button>
                    </div>
                  )}
                </div>

                {error && (
                  <div className="bg-red-50 border border-red-200 rounded-md p-3">
                    <p className="text-sm text-red-600">{error}</p>
                  </div>
                )}

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
                >
                  {loading ? "Loading..." : (isSignup ? "Sign Up" : "Login")}
                </button>
              </form>

              {/* Action buttons - positioned prominently */}
              <div className="mt-6 text-center border-t border-gray-100 pt-6">
                <p className="text-sm text-gray-600">
                  {isSignup ? "Already have an account?" : "Don't have an account?"}{" "}
                  <button
                    onClick={() => setIsSignup(!isSignup)}
                    className="text-blue-600 hover:text-blue-500 font-medium transition-colors duration-200"
                  >
                    {isSignup ? "Login" : "Sign Up"}
                  </button>
                </p>
              </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 