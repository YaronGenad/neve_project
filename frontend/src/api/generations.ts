import apiClient from './client';
import {
  GenerationResponse,
  GenerationStatus,
  GenerationListResponse,
  SubmitGenerationData,
} from '../types';

export const submitGeneration = async (data: SubmitGenerationData): Promise<GenerationResponse> => {
  const response = await apiClient.post<GenerationResponse>('/generations/', data);
  return response.data;
};

export const getGenerations = async (
  limit = 20,
  offset = 0
): Promise<GenerationListResponse> => {
  const response = await apiClient.get<GenerationListResponse>('/generations/', {
    params: { limit, offset },
  });
  return response.data;
};

export const getGeneration = async (id: string): Promise<GenerationStatus> => {
  const response = await apiClient.get<GenerationStatus>(`/generations/${id}`);
  return response.data;
};

export const downloadFile = async (generationId: string, fileType: string): Promise<void> => {
  const response = await apiClient.get(
    `/generations/${generationId}/download/${fileType}`,
    { responseType: 'blob' }
  );

  // Extract filename from Content-Disposition header if available
  const contentDisposition = response.headers['content-disposition'];
  let filename = `${fileType}.pdf`;
  if (contentDisposition) {
    const match = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
    if (match?.[1]) {
      filename = match[1].replace(/['"]/g, '');
    }
  }

  // Create a temporary URL and trigger download
  const url = URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
};
