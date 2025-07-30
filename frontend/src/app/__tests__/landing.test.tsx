import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { useRouter } from 'next/navigation';
import axios from 'axios';
import LandingPage from '../landing/page';

// Mock Next.js router
jest.mock('next/navigation', () => ({
  useRouter: jest.fn(),
}));

// Mock axios
jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};
global.localStorage = localStorageMock;

describe('LandingPage', () => {
  const mockPush = jest.fn();
  
  beforeEach(() => {
    jest.clearAllMocks();
    (useRouter as jest.Mock).mockReturnValue({
      push: mockPush,
    });
  });

  describe('Rendering', () => {
    it('renders the landing page with signup form by default', () => {
      render(<LandingPage />);
      
      expect(screen.getByText('Master SQL with')).toBeInTheDocument();
      expect(screen.getByText('Interactive Challenges')).toBeInTheDocument();
      expect(screen.getByText('Create Your Account')).toBeInTheDocument();
      expect(screen.getByLabelText('Email Address')).toBeInTheDocument();
      expect(screen.getByLabelText('Password')).toBeInTheDocument();
      expect(screen.getByRole('button', { name: 'Sign Up' })).toBeInTheDocument();
    });

    it('shows login form when login button is clicked', () => {
      render(<LandingPage />);
      
      const loginButton = screen.getByRole('button', { name: 'Login' });
      fireEvent.click(loginButton);
      
      expect(screen.getByText('Welcome Back')).toBeInTheDocument();
      expect(screen.getByRole('button', { name: 'Login' })).toBeInTheDocument();
    });

    it('shows signup form when signup button is clicked', () => {
      render(<LandingPage />);
      
      // First switch to login
      const loginButton = screen.getByRole('button', { name: 'Login' });
      fireEvent.click(loginButton);
      
      // Then switch back to signup
      const signupButton = screen.getByRole('button', { name: 'Sign Up' });
      fireEvent.click(signupButton);
      
      expect(screen.getByText('Create Your Account')).toBeInTheDocument();
    });

    it('displays features section', () => {
      render(<LandingPage />);
      
      expect(screen.getByText('Instant Feedback')).toBeInTheDocument();
      expect(screen.getByText('Real Database Schema')).toBeInTheDocument();
      expect(screen.getByText('Progressive Learning')).toBeInTheDocument();
    });
  });

  describe('Form Interaction', () => {
    it('updates email input value', () => {
      render(<LandingPage />);
      
      const emailInput = screen.getByLabelText('Email Address');
      fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
      
      expect(emailInput).toHaveValue('test@example.com');
    });

    it('updates password input value', () => {
      render(<LandingPage />);
      
      const passwordInput = screen.getByLabelText('Password');
      fireEvent.change(passwordInput, { target: { value: 'password123' } });
      
      expect(passwordInput).toHaveValue('password123');
    });

    it('shows loading state when form is submitted', async () => {
      mockedAxios.post.mockResolvedValueOnce({
        data: {
          access_token: 'mock-token',
          token_type: 'bearer',
          email: 'test@example.com',
        },
      });

      render(<LandingPage />);
      
      const emailInput = screen.getByLabelText('Email Address');
      const passwordInput = screen.getByLabelText('Password');
      const submitButton = screen.getByRole('button', { name: 'Sign Up' });
      
      fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
      fireEvent.change(passwordInput, { target: { value: 'password123' } });
      fireEvent.click(submitButton);
      
      expect(screen.getByText('Loading...')).toBeInTheDocument();
    });
  });

  describe('Authentication', () => {
    it('handles successful signup', async () => {
      mockedAxios.post.mockResolvedValueOnce({
        data: {
          access_token: 'mock-token',
          token_type: 'bearer',
          email: 'test@example.com',
        },
      });

      render(<LandingPage />);
      
      const emailInput = screen.getByLabelText('Email Address');
      const passwordInput = screen.getByLabelText('Password');
      const submitButton = screen.getByRole('button', { name: 'Sign Up' });
      
      fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
      fireEvent.change(passwordInput, { target: { value: 'password123' } });
      fireEvent.click(submitButton);
      
      await waitFor(() => {
        expect(localStorage.setItem).toHaveBeenCalledWith('token', 'mock-token');
        expect(localStorage.setItem).toHaveBeenCalledWith('userEmail', 'test@example.com');
        expect(mockPush).toHaveBeenCalledWith('/challenges');
      });
    });

    it('handles successful login', async () => {
      mockedAxios.post.mockResolvedValueOnce({
        data: {
          access_token: 'mock-token',
          token_type: 'bearer',
          email: 'test@example.com',
        },
      });

      render(<LandingPage />);
      
      // Switch to login form
      const loginButton = screen.getByRole('button', { name: 'Login' });
      fireEvent.click(loginButton);
      
      const emailInput = screen.getByLabelText('Email Address');
      const passwordInput = screen.getByLabelText('Password');
      const submitButton = screen.getByRole('button', { name: 'Login' });
      
      fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
      fireEvent.change(passwordInput, { target: { value: 'password123' } });
      fireEvent.click(submitButton);
      
      await waitFor(() => {
        expect(localStorage.setItem).toHaveBeenCalledWith('token', 'mock-token');
        expect(localStorage.setItem).toHaveBeenCalledWith('userEmail', 'test@example.com');
        expect(mockPush).toHaveBeenCalledWith('/challenges');
      });
    });

    it('handles authentication error', async () => {
      mockedAxios.post.mockRejectedValueOnce({
        response: {
          data: {
            detail: 'Email already registered',
          },
        },
      });

      render(<LandingPage />);
      
      const emailInput = screen.getByLabelText('Email Address');
      const passwordInput = screen.getByLabelText('Password');
      const submitButton = screen.getByRole('button', { name: 'Sign Up' });
      
      fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
      fireEvent.change(passwordInput, { target: { value: 'password123' } });
      fireEvent.click(submitButton);
      
      await waitFor(() => {
        expect(screen.getByText('Email already registered')).toBeInTheDocument();
      });
    });

    it('handles network error', async () => {
      mockedAxios.post.mockRejectedValueOnce(new Error('Network error'));

      render(<LandingPage />);
      
      const emailInput = screen.getByLabelText('Email Address');
      const passwordInput = screen.getByLabelText('Password');
      const submitButton = screen.getByRole('button', { name: 'Sign Up' });
      
      fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
      fireEvent.change(passwordInput, { target: { value: 'password123' } });
      fireEvent.click(submitButton);
      
      await waitFor(() => {
        expect(screen.getByText('An error occurred')).toBeInTheDocument();
      });
    });
  });

  describe('Form Validation', () => {
    it('prevents submission with empty fields', () => {
      render(<LandingPage />);
      
      const submitButton = screen.getByRole('button', { name: 'Sign Up' });
      fireEvent.click(submitButton);
      
      // Form should not submit without required fields
      expect(mockedAxios.post).not.toHaveBeenCalled();
    });

    it('prevents submission with invalid email', () => {
      render(<LandingPage />);
      
      const emailInput = screen.getByLabelText('Email Address');
      const passwordInput = screen.getByLabelText('Password');
      const submitButton = screen.getByRole('button', { name: 'Sign Up' });
      
      fireEvent.change(emailInput, { target: { value: 'invalid-email' } });
      fireEvent.change(passwordInput, { target: { value: 'password123' } });
      fireEvent.click(submitButton);
      
      // Form should not submit with invalid email
      expect(mockedAxios.post).not.toHaveBeenCalled();
    });
  });

  describe('Navigation', () => {
    it('switches between signup and login forms', () => {
      render(<LandingPage />);
      
      // Initially shows signup
      expect(screen.getByText('Create Your Account')).toBeInTheDocument();
      
      // Switch to login
      const loginButton = screen.getByRole('button', { name: 'Login' });
      fireEvent.click(loginButton);
      expect(screen.getByText('Welcome Back')).toBeInTheDocument();
      
      // Switch back to signup
      const signupLink = screen.getByText('Sign Up');
      fireEvent.click(signupLink);
      expect(screen.getByText('Create Your Account')).toBeInTheDocument();
    });
  });
}); 