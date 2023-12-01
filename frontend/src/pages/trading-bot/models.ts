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
  trade_history: BotDetailsProps[]
}

export interface ApiResponse {
  data: Bot[];
}

export interface BotDetailsProps {
  id: number;
  container_name: string;
  action: string;
  order_id: number;
  qty: number;
  avg_price: number;
  realizedPnl: number;
  totalRealizedPnl: number;
  info: {
    side: string;
    type: string;
    symbol: string;
    // ... other properties ...
  };
  timestamp: number;
}
