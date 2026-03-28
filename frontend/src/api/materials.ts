import apiClient from './client';
import {
  MaterialApprovalResponse,
  MaterialVersionsResponse,
} from '../types';

export const approveMaterial = async (
  materialId: string
): Promise<MaterialApprovalResponse> => {
  const response = await apiClient.post<MaterialApprovalResponse>(
    `/materials/${materialId}/approve`
  );
  return response.data;
};

export const rejectMaterial = async (
  materialId: string
): Promise<MaterialApprovalResponse> => {
  const response = await apiClient.post<MaterialApprovalResponse>(
    `/materials/${materialId}/reject`
  );
  return response.data;
};

export const getMaterialVersions = async (
  subject: string,
  topic: string,
  grade: string
): Promise<MaterialVersionsResponse> => {
  const response = await apiClient.get<MaterialVersionsResponse>(
    '/materials/versions',
    { params: { subject, topic, grade } }
  );
  return response.data;
};
