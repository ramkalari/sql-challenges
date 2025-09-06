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
      
      // Check for redirect parameter
      const urlParams = new URLSearchParams(window.location.search);
      const redirectTo = urlParams.get("redirect");
      
      if (redirectTo) {
        router.push(redirectTo);
      } else {
        // Default redirect to home page (courses)
        router.push("/");
      }
    } catch (err: unknown) {
      const error = err as ApiError;
      setError(error.response?.data?.detail || "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-900">Brickwall Academy</h1>
          <p className="mt-2 text-sm text-gray-600">
            Master technology through interactive challenges
          </p>
        </div>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow-lg sm:rounded-lg sm:px-10">
          {/* Tab Navigation */}
          <div className="flex mb-6">
            <button
              onClick={() => setIsSignup(false)}
              className={`flex-1 py-2 px-4 text-sm font-medium rounded-l-md transition-all duration-200 ${
                !isSignup
                  ? "bg-blue-600 text-white"
                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"
              }`}
            >
              Sign In
            </button>
            <button
              onClick={() => setIsSignup(true)}
              className={`flex-1 py-2 px-4 text-sm font-medium rounded-r-md transition-all duration-200 ${
                isSignup
                  ? "bg-blue-600 text-white"
                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"
              }`}
            >
              Sign Up
            </button>
          </div>

          {/* Form */}
          <form className="space-y-6" onSubmit={handleSubmit}>
            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md text-sm">
                {error}
              </div>
            )}

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                Email address
              </label>
              <div className="mt-1">
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  placeholder="Enter your email"
                />
              </div>
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                Password
              </label>
              <div className="mt-1">
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete={isSignup ? "new-password" : "current-password"}
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  placeholder="Enter your password"
                />
              </div>
            </div>

            <div>
              <button
                type="submit"
                disabled={loading}
                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
              >
                {loading ? (
                  <div className="flex items-center">
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                    {isSignup ? "Creating Account..." : "Signing In..."}
                  </div>
                ) : (
                  isSignup ? "Create Account" : "Sign In"
                )}
              </button>
            </div>
          </form>

          {/* Footer Links */}
          <div className="mt-6">
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-300" />
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 bg-white text-gray-500">
                  {isSignup ? "Already have an account?" : "Don't have an account?"}
                </span>
              </div>
            </div>

            <div className="mt-6 text-center">
              <button
                onClick={() => setIsSignup(!isSignup)}
                className="text-blue-600 hover:text-blue-500 text-sm font-medium"
              >
                {isSignup ? "Sign in instead" : "Create an account"}
              </button>
            </div>
          </div>

          {/* Forgot Password Link */}
          {!isSignup && (
            <div className="mt-4 text-center">
              <button
                onClick={() => router.push("/forgot-password")}
                className="text-sm text-gray-600 hover:text-gray-500"
              >
                Forgot your password?
              </button>
            </div>
          )}
        </div>

        {/* Motivational Quote */}
        <div className="mt-8 text-center">
          <div className="bg-white rounded-lg shadow-sm p-6">
            <blockquote className="text-lg text-gray-700 italic">
              &ldquo;The brick walls are there for a reason. They give us a chance to show how badly we want something.&rdquo;
            </blockquote>
            <cite className="block mt-2 text-sm text-gray-500">
              — Randy Pausch
            </cite>
          </div>
        </div>
      </div>
    </div>
  );
} 