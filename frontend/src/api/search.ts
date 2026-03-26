import apiClient from './client';
import { SearchResponse } from '../types';

export const searchSimilar = async (
  query: string,
  topK = 5,
  threshold = 1.0
): Promise<SearchResponse> => {
  const response = await apiClient.get<SearchResponse>('/search/', {
    params: { q: query, top_k: topK, threshold },
  });
  return response.data;
};
