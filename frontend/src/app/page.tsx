"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";

interface Course {
  id: string;
  name: string;
  description: string;
  icon: string;
  difficulty: string;
  duration: string;
  features: string[];
  technologies: string[];
  challenge_count: number;
  is_available: boolean;
}

interface ApiError {
  response?: {
    status: number;
    data?: {
      detail?: string;
    };
  };
}

export default function Home() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [userEmail, setUserEmail] = useState("");
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const router = useRouter();

  useEffect(() => {
    // Check if user is authenticated
    const token = localStorage.getItem("token");
    const email = localStorage.getItem("userEmail");
    
    if (token && email) {
      setIsAuthenticated(true);
      setUserEmail(email);
      // Set up axios defaults for authenticated requests
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
    }

    // Fetch courses (available to all users)
    const fetchCourses = async () => {
      try {
        const res = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/courses`);
        setCourses(res.data.courses);
      } catch (err: unknown) {
        const error = err as ApiError;
        setError("Failed to load courses.");
        console.error("Error loading courses:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchCourses();
  }, []);

  const handleCourseClick = (courseId: string, isAvailable: boolean) => {
    if (!isAvailable) {
      return; // Do nothing for unavailable courses
    }

    if (!isAuthenticated) {
      // Redirect to login with course ID in query params
      router.push(`/landing?redirect=/courses/${courseId}`);
      return;
    }

    // Navigate to course challenges
    router.push(`/courses/${courseId}`);
  };

  const handleLogin = () => {
    router.push("/landing");
  };

  const handleProfile = () => {
    router.push("/profile");
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("userEmail");
    setIsAuthenticated(false);
    setUserEmail("");
    delete axios.defaults.headers.common["Authorization"];
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading courses...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-gray-900">Brickwall Academy</h1>
            </div>
            <div className="flex items-center space-x-4">
              {isAuthenticated ? (
                <>
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
                </>
              ) : (
                <button
                  onClick={handleLogin}
                  className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700"
                >
                  Login
                </button>
              )}
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-4xl font-bold text-gray-900 sm:text-5xl md:text-6xl">
            Master Technology
            <span className="block text-blue-600">One Challenge at a Time</span>
          </h1>
          <p className="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
            Interactive coding challenges designed to help you learn and practice programming skills through hands-on experience.
          </p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-8 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}

        {/* Courses Grid */}
        <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-2">
          {courses.map((course) => (
            <div
              key={course.id}
              onClick={() => handleCourseClick(course.id, course.is_available)}
              className={`relative bg-white rounded-lg shadow-lg overflow-hidden transition-transform duration-200 ${
                course.is_available 
                  ? "hover:scale-105 cursor-pointer hover:shadow-xl" 
                  : "opacity-75 cursor-not-allowed"
              }`}
            >
              {!course.is_available && (
                <div className="absolute top-4 right-4 bg-yellow-100 text-yellow-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
                  Coming Soon
                </div>
              )}
              
              <div className="p-6">
                <div className="flex items-center mb-4">
                  <span className="text-4xl mr-4">{course.icon}</span>
                  <div>
                    <h3 className="text-xl font-bold text-gray-900">{course.name}</h3>
                    <p className="text-sm text-gray-500">{course.difficulty} • {course.duration}</p>
                  </div>
                </div>
                
                <p className="text-gray-600 mb-4">{course.description}</p>
                
                {/* Features */}
                <div className="mb-4">
                  <h4 className="text-sm font-semibold text-gray-900 mb-2">What you'll learn:</h4>
                  <ul className="text-sm text-gray-600 space-y-1">
                    {course.features.slice(0, 3).map((feature, index) => (
                      <li key={index} className="flex items-center">
                        <span className="text-green-500 mr-2">✓</span>
                        {feature}
                      </li>
                    ))}
                  </ul>
                </div>
                
                {/* Technologies */}
                <div className="mb-4">
                  <div className="flex flex-wrap gap-2">
                    {course.technologies.map((tech, index) => (
                      <span
                        key={index}
                        className="inline-block bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded-full"
                      >
                        {tech}
                      </span>
                    ))}
                  </div>
                </div>
                
                {/* Challenge Count */}
                {course.is_available && (
                  <div className="text-sm text-gray-500">
                    {course.challenge_count} challenge{course.challenge_count !== 1 ? 's' : ''}
                  </div>
                )}
              </div>
              
              {course.is_available && (
                <div className="px-6 py-4 bg-gray-50">
                  <button className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors duration-200">
                    {isAuthenticated ? 'Start Learning' : 'Login to Start'}
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Call to Action */}
        {!isAuthenticated && (
          <div className="mt-16 text-center">
            <div className="bg-white rounded-lg shadow-lg p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">
                Ready to Start Learning?
              </h2>
              <p className="text-gray-600 mb-6">
                Join thousands of developers improving their skills with our interactive challenges.
              </p>
              <button
                onClick={handleLogin}
                className="bg-blue-600 text-white px-8 py-3 rounded-md text-lg font-medium hover:bg-blue-700 transition-colors duration-200"
              >
                Get Started Today
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

