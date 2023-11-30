import React, { useState, useEffect } from "react";
import { matchPath } from "react-router-dom";

// Define an interface for the candlestick data
interface MarkPriceData {
  e: string; // Event type
  E: number; // Event time
  s: string; // Symbol
  p: string; // Mark price
  // ... other fields ...
}
const BinancePrices: React.FC = () => {
  const [ethPrice, setEthPrice] = useState<string[] | null>(null);
  //   const [btcPrice, setBtcPrice] = useState<string | null>(null);

  useEffect(() => {
    // Initialize WebSocket connections
    const ethWs = new WebSocket(
      //   "wss://fstream.binance.com/ws/ethusdt@markPrice"
      "wss://fstream.binance.com/ws/!markPrice@arr"
    );
    // const btcWs = new WebSocket(
    //   "wss://stream.binance.com:9443/ws/btcusdt@markPrice@3s/bnbusdt@markPrice@3s"
    // );

    // Handle ETH WebSocket messages
    ethWs.onmessage = (event) => {
      console.log("Hi from binance ws", event);

      const message: MarkPriceData[] = JSON.parse(event.data);
      setEthPrice(message.filter((m) => m.s === "ETHUSDT").map((m) => m.p));
    };

    // Handle BTC WebSocket messages
    // btcWs.onmessage = (event: MessageEvent) => {
    //   const message: MarkPriceData = JSON.parse(event.data);
    //   const { c: closePrice, x: isClosed } = message.k;

    //   if (isClosed) {
    //     setBtcPrice(closePrice);
    //   }
    // };

    // Clean up function
    return () => {
      ethWs.close();
      //   btcWs.close();
    };
  }, []);

  return (
    <div>
      <h1>Cryptocurrency Prices</h1>
      <p>ETH/USDT: {ethPrice ? `${ethPrice}` : "Loading..."}</p>
      {/* <p>BTC/USDT: {btcPrice ? `$${btcPrice}` : "Loading..."}</p> */}
    </div>
  );
};

export default BinancePrices;
