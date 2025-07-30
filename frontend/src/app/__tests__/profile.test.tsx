import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { useRouter } from 'next/navigation';
import axios from 'axios';
import ProfilePage from '../profile/page';

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
  length: 0,
  key: jest.fn(),
};
global.localStorage = localStorageMock;

describe('ProfilePage', () => {
  const mockPush = jest.fn();
  
  beforeEach(() => {
    jest.clearAllMocks();
    (useRouter as jest.Mock).mockReturnValue({
      push: mockPush,
    });
  });

  describe('Authentication', () => {
    it('redirects to landing page when not authenticated', () => {
      localStorageMock.getItem.mockReturnValue(null);
      
      render(<ProfilePage />);
      
      expect(mockPush).toHaveBeenCalledWith('/landing');
    });

    it('redirects to landing page when token is invalid', async () => {
      localStorageMock.getItem.mockReturnValue('mock-token');
      mockedAxios.get.mockRejectedValueOnce({
        response: { status: 401 },
      });
      
      render(<ProfilePage />);
      
      await waitFor(() => {
        expect(localStorage.removeItem).toHaveBeenCalledWith('token');
        expect(localStorage.removeItem).toHaveBeenCalledWith('userEmail');
        expect(mockPush).toHaveBeenCalledWith('/landing');
      });
    });
  });

  describe('Rendering', () => {
    beforeEach(() => {
      localStorageMock.getItem.mockReturnValue('mock-token');
      mockedAxios.get.mockResolvedValueOnce({
        data: {
          progress: [
            {
              challenge_id: 1,
              challenge_name: 'Select All Products',
              level: 'Basic',
              solved_at: '2024-01-01T10:00:00Z',
              attempts: 2,
            },
          ],
        },
      });
      mockedAxios.get.mockResolvedValueOnce({
        data: {
          submissions: [
            {
              challenge_id: 1,
              challenge_name: 'Select All Products',
              query: 'SELECT * FROM products',
              passed: true,
              submitted_at: '2024-01-01T10:00:00Z',
            },
          ],
        },
      });
    });

    it('renders profile page with user data', async () => {
      render(<ProfilePage />);
      
      await waitFor(() => {
        expect(screen.getByText('Profile')).toBeInTheDocument();
        expect(screen.getByText('Back to Challenges')).toBeInTheDocument();
      });
    });

    it('displays progress statistics', async () => {
      render(<ProfilePage />);
      
      await waitFor(() => {
        expect(screen.getByText('Challenges Solved')).toBeInTheDocument();
        expect(screen.getByText('Total Submissions')).toBeInTheDocument();
        expect(screen.getByText('Success Rate')).toBeInTheDocument();
      });
    });

    it('shows solved challenges', async () => {
      render(<ProfilePage />);
      
      await waitFor(() => {
        expect(screen.getByText('Select All Products')).toBeInTheDocument();
        expect(screen.getByText('Basic')).toBeInTheDocument();
      });
    });

    it('shows recent submissions', async () => {
      render(<ProfilePage />);
      
      await waitFor(() => {
        expect(screen.getByText('Recent Submissions')).toBeInTheDocument();
        expect(screen.getByText('SELECT * FROM products')).toBeInTheDocument();
      });
    });
  });

  describe('Navigation', () => {
    beforeEach(() => {
      localStorageMock.getItem.mockReturnValue('mock-token');
      mockedAxios.get.mockResolvedValueOnce({
        data: { progress: [] },
      });
      mockedAxios.get.mockResolvedValueOnce({
        data: { submissions: [] },
      });
    });

    it('navigates back to challenges', async () => {
      render(<ProfilePage />);
      
      await waitFor(() => {
        const backButton = screen.getByText('Back to Challenges');
        fireEvent.click(backButton);
        expect(mockPush).toHaveBeenCalledWith('/challenges');
      });
    });

    it('logs out user', async () => {
      render(<ProfilePage />);
      
      await waitFor(() => {
        const logoutButton = screen.getByText('Logout');
        fireEvent.click(logoutButton);
        
        expect(localStorage.removeItem).toHaveBeenCalledWith('token');
        expect(localStorage.removeItem).toHaveBeenCalledWith('userEmail');
        expect(mockPush).toHaveBeenCalledWith('/landing');
      });
    });
  });

  describe('Empty States', () => {
    beforeEach(() => {
      localStorageMock.getItem.mockReturnValue('mock-token');
      mockedAxios.get.mockResolvedValueOnce({
        data: { progress: [] },
      });
      mockedAxios.get.mockResolvedValueOnce({
        data: { submissions: [] },
      });
    });

    it('shows empty state for no solved challenges', async () => {
      render(<ProfilePage />);
      
      await waitFor(() => {
        expect(screen.getByText('No challenges solved yet. Start practicing!')).toBeInTheDocument();
      });
    });

    it('shows empty state for no submissions', async () => {
      render(<ProfilePage />);
      
      await waitFor(() => {
        expect(screen.getByText('No submissions yet. Start solving challenges!')).toBeInTheDocument();
      });
    });
  });

  describe('Error Handling', () => {
    beforeEach(() => {
      localStorageMock.getItem.mockReturnValue('mock-token');
    });

    it('handles API errors gracefully', async () => {
      mockedAxios.get.mockRejectedValueOnce(new Error('Network error'));
      
      render(<ProfilePage />);
      
      await waitFor(() => {
        expect(screen.getByText('Failed to load profile data.')).toBeInTheDocument();
      });
    });
  });
}); 