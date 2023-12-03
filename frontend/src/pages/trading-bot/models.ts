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
  trade_history: BotDetailsProps[];
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
    cumQuote: string;
    // ... other properties ...
  };
  timestamp: number;
}

export interface ContainerStateProps {
  bot_id: number
  container_id: string;
  container_name: string;
  state: string;
  status: string;
  running_for: string;
  logs: Array<string>;
  updated_at: string;
}

export interface MarkPriceData {
  e: string; // Event type
  E: number; // Event time
  s: string; // Symbol
  p: string; // Mark price
  // ... other fields ...
}

export interface BotError {
  id: number;
  container_name: string;
  error: string;
  timestamp: string;
}
