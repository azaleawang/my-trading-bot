import React, { useEffect, useContext } from "react";
import { TradingDataContext } from "../../../../common/hooks/TradingDataContext";

// Define an interface for the candlestick data
interface MarkPriceData {
  e: string; // Event type
  E: number; // Event time
  s: string; // Symbol
  p: string; // Mark price
  // ... other fields ...
}
// TODO 現在只有處理一個交易對的及時資料
const BinancePrices: React.FC = () => {
  // const [markPrice, setMarkPrice] = useState<string[] | null>(null);

  const { markPrice, setMarkPrice } = useContext(TradingDataContext);
  useEffect(() => {
    // Initialize WebSocket connections
    const markPriceWs = new WebSocket(
      "wss://fstream.binance.com/ws/!markPrice@arr"
    );
    // const btcWs = new WebSocket(
    //   "wss://stream.binance.com:9443/ws/btcusdt@markPrice/bnbusdt@markPrice"
    // );

    // Handle ETH WebSocket messages
    markPriceWs.onmessage = (event) => {
      console.log("Hi from binance ws", event);

      const message: MarkPriceData[] = JSON.parse(event.data);
      setMarkPrice(message.filter((m) => m.s === "ETHUSDT").map((m) => m.p));
    };

    // Clean up function
    return () => {
      markPriceWs.close();
    };
  }, []);

  return (
    <div>
      <h1>Cryptocurrency Prices</h1>
      <p>ETH/USDT: {markPrice ? `${markPrice}` : "Loading..."}</p>
    </div>
  );
};

export default BinancePrices;
