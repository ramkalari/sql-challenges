import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { useRouter } from 'next/navigation';
import axios from 'axios';
import ChallengesPage from '../challenges/page';

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

describe('ChallengesPage', () => {
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
      
      render(<ChallengesPage />);
      
      expect(mockPush).toHaveBeenCalledWith('/landing');
    });

    it('redirects to landing page when token is invalid', async () => {
      localStorageMock.getItem.mockReturnValue('mock-token');
      mockedAxios.get.mockRejectedValueOnce({
        response: { status: 401 },
      });
      
      render(<ChallengesPage />);
      
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
        data: [
          {
            id: 1,
            name: 'Select All Products',
            level: 'Basic',
            solved: false,
            attempts: 0,
          },
          {
            id: 2,
            name: 'Select Name and Price',
            level: 'Basic',
            solved: true,
            attempts: 3,
          },
        ],
      });
    });

    it('renders challenges list when authenticated', async () => {
      render(<ChallengesPage />);
      
      await waitFor(() => {
        expect(screen.getByText('Select All Products')).toBeInTheDocument();
        expect(screen.getByText('Select Name and Price')).toBeInTheDocument();
      });
    });

    it('displays progress statistics', async () => {
      render(<ChallengesPage />);
      
      await waitFor(() => {
        expect(screen.getByText('1 of 2 solved')).toBeInTheDocument();
      });
    });

    it('shows solved challenges with checkmark', async () => {
      render(<ChallengesPage />);
      
      await waitFor(() => {
        const solvedChallenge = screen.getByText('Select Name and Price').closest('button');
        expect(solvedChallenge).toHaveClass('bg-blue-50');
      });
    });

    it('shows attempt counts', async () => {
      render(<ChallengesPage />);
      
      await waitFor(() => {
        expect(screen.getByText('3 attempts')).toBeInTheDocument();
      });
    });
  });

  describe('Challenge Selection', () => {
    beforeEach(() => {
      localStorageMock.getItem.mockReturnValue('mock-token');
      mockedAxios.get.mockResolvedValueOnce({
        data: [
          {
            id: 1,
            name: 'Select All Products',
            level: 'Basic',
            solved: false,
            attempts: 0,
          },
        ],
      });
    });

    it('loads challenge details when selected', async () => {
      mockedAxios.get.mockResolvedValueOnce({
        data: {
          id: 1,
          name: 'Select All Products',
          level: 'Basic',
          question: 'Write a query to select all products',
          schema_tables: [
            {
              table_name: 'products',
              columns: [
                { name: 'id', type: 'INTEGER', constraints: ['PRIMARY KEY'] },
                { name: 'name', type: 'TEXT', constraints: [] },
              ],
            },
          ],
        },
      });

      render(<ChallengesPage />);
      
      await waitFor(() => {
        const challengeButton = screen.getByText('Select All Products');
        fireEvent.click(challengeButton);
      });

      await waitFor(() => {
        expect(screen.getByText('Write a query to select all products')).toBeInTheDocument();
        expect(screen.getByText('Table: products')).toBeInTheDocument();
      });
    });

    it('shows empty state when no challenge is selected', async () => {
      render(<ChallengesPage />);
      
      await waitFor(() => {
        expect(screen.getByText('Select a Challenge')).toBeInTheDocument();
        expect(screen.getByText('Choose a challenge from the sidebar to start practicing SQL queries.')).toBeInTheDocument();
      });
    });
  });

  describe('Query Submission', () => {
    beforeEach(() => {
      localStorageMock.getItem.mockReturnValue('mock-token');
      mockedAxios.get.mockResolvedValueOnce({
        data: [
          {
            id: 1,
            name: 'Select All Products',
            level: 'Basic',
            solved: false,
            attempts: 0,
          },
        ],
      });
    });

    it('submits correct query successfully', async () => {
      mockedAxios.get.mockResolvedValueOnce({
        data: {
          id: 1,
          name: 'Select All Products',
          level: 'Basic',
          question: 'Write a query to select all products',
          schema_tables: [],
        },
      });

      mockedAxios.post.mockResolvedValueOnce({
        data: {
          passed: true,
          result: [['1', 'Laptop', '1200', 'Electronics']],
          column_names: ['id', 'name', 'price', 'category'],
        },
      });

      render(<ChallengesPage />);
      
      // Select challenge
      await waitFor(() => {
        const challengeButton = screen.getByText('Select All Products');
        fireEvent.click(challengeButton);
      });

      // Submit query
      await waitFor(() => {
        const queryInput = screen.getByPlaceholderText('Write your SQL query here...');
        const submitButton = screen.getByText('Run Query');
        
        fireEvent.change(queryInput, { target: { value: 'SELECT * FROM products' } });
        fireEvent.click(submitButton);
      });

      await waitFor(() => {
        expect(screen.getByText('✅ Passed')).toBeInTheDocument();
        expect(screen.getByText('Your Result')).toBeInTheDocument();
      });
    });

    it('handles incorrect query submission', async () => {
      mockedAxios.get.mockResolvedValueOnce({
        data: {
          id: 1,
          name: 'Select All Products',
          level: 'Basic',
          question: 'Write a query to select all products',
          schema_tables: [],
        },
      });

      mockedAxios.post.mockResolvedValueOnce({
        data: {
          passed: false,
          result: [['Laptop']],
          expected: [['1', 'Laptop', '1200', 'Electronics']],
          column_names: ['name'],
          expected_column_names: ['id', 'name', 'price', 'category'],
        },
      });

      render(<ChallengesPage />);
      
      // Select challenge
      await waitFor(() => {
        const challengeButton = screen.getByText('Select All Products');
        fireEvent.click(challengeButton);
      });

      // Submit query
      await waitFor(() => {
        const queryInput = screen.getByPlaceholderText('Write your SQL query here...');
        const submitButton = screen.getByText('Run Query');
        
        fireEvent.change(queryInput, { target: { value: 'SELECT name FROM products' } });
        fireEvent.click(submitButton);
      });

      await waitFor(() => {
        expect(screen.getByText('❌ Failed')).toBeInTheDocument();
        expect(screen.getByText('Your Result')).toBeInTheDocument();
        expect(screen.getByText('Expected Result')).toBeInTheDocument();
      });
    });

    it('handles query submission error', async () => {
      mockedAxios.get.mockResolvedValueOnce({
        data: {
          id: 1,
          name: 'Select All Products',
          level: 'Basic',
          question: 'Write a query to select all products',
          schema_tables: [],
        },
      });

      mockedAxios.post.mockRejectedValueOnce({
        response: {
          data: {
            detail: 'Invalid SQL syntax',
          },
        },
      });

      render(<ChallengesPage />);
      
      // Select challenge
      await waitFor(() => {
        const challengeButton = screen.getByText('Select All Products');
        fireEvent.click(challengeButton);
      });

      // Submit query
      await waitFor(() => {
        const queryInput = screen.getByPlaceholderText('Write your SQL query here...');
        const submitButton = screen.getByText('Run Query');
        
        fireEvent.change(queryInput, { target: { value: 'SELECT * FROM' } });
        fireEvent.click(submitButton);
      });

      await waitFor(() => {
        expect(screen.getByText('Invalid SQL syntax')).toBeInTheDocument();
      });
    });
  });

  describe('Navigation', () => {
    beforeEach(() => {
      localStorageMock.getItem.mockReturnValue('mock-token');
      mockedAxios.get.mockResolvedValueOnce({
        data: [
          {
            id: 1,
            name: 'Select All Products',
            level: 'Basic',
            solved: false,
            attempts: 0,
          },
        ],
      });
    });

    it('navigates to profile page', async () => {
      render(<ChallengesPage />);
      
      await waitFor(() => {
        const profileButton = screen.getByText('Profile');
        fireEvent.click(profileButton);
        expect(mockPush).toHaveBeenCalledWith('/profile');
      });
    });

    it('logs out user', async () => {
      render(<ChallengesPage />);
      
      await waitFor(() => {
        const logoutButton = screen.getByText('Logout');
        fireEvent.click(logoutButton);
        
        expect(localStorage.removeItem).toHaveBeenCalledWith('token');
        expect(localStorage.removeItem).toHaveBeenCalledWith('userEmail');
        expect(mockPush).toHaveBeenCalledWith('/landing');
      });
    });
  });

  describe('Responsive Design', () => {
    beforeEach(() => {
      localStorageMock.getItem.mockReturnValue('mock-token');
      mockedAxios.get.mockResolvedValueOnce({
        data: [
          {
            id: 1,
            name: 'Select All Products',
            level: 'Basic',
            solved: false,
            attempts: 0,
          },
        ],
      });
    });

    it('renders with responsive classes', async () => {
      render(<ChallengesPage />);
      
      await waitFor(() => {
        const mainContainer = screen.getByText('Select All Products').closest('div');
        expect(mainContainer).toHaveClass('flex-col', 'lg:flex-row');
      });
    });
  });
}); 