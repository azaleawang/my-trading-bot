// interfaces for current folder
export interface Bot {
  name: string;
  strategy: string;
  symbol: string;
  description: string;
  created_at: string;
  owner_id: number;
  container_id: string;
  container_name: string;
  status: string;
  id: number;
}

export interface ApiResponse {
  data: Bot[];
}
