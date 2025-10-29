import axios from 'axios';
import { ChatResponse } from '../types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export const chatAPI = {
  /**
   * Send a message to the AI backend
   */
  sendMessage: async (message: string): Promise<ChatResponse> => {
    try {
      const response = await axios.post<ChatResponse>(
        `${API_URL}/api/chat`,
        { message },
        {
          headers: {
            'Content-Type': 'application/json',
          },
          timeout: 60000, // 60 second timeout for AI responses
        }
      );
      
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        return {
          success: false,
          error: error.response?.data?.error || error.message || 'Failed to connect to backend',
        };
      }
      return {
        success: false,
        error: 'An unexpected error occurred',
      };
    }
  },

  /**
   * Check backend health
   */
  healthCheck: async (): Promise<boolean> => {
    try {
      const response = await axios.get(`${API_URL}/api/health`, {
        timeout: 5000,
      });
      return response.data.status === 'healthy';
    } catch {
      return false;
    }
  },
};
