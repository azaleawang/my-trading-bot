import { useState, useEffect } from "react";
import axios from "axios";
import BacktestResult from "../data";
import StrategyForm from "../../../run-backtest/components/strategy-form";

const Backtest = () => {
  const [backtestData, setBacktestData] = useState();
  const [backtestId, setBacktestId] = useState(null);
  useEffect(() => {
    const socket = new WebSocket(`${import.meta.env.VITE_WS_HOST}/ws/backtest_result`);

    socket.onopen = () => {
      console.log("WebSocket Connected");
    };

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log("Parsed data:", data.id);
        setBacktestId(data.id);

      } catch (error) {
        console.error("Error parsing message:", error);
      }
    };

    socket.onerror = (error) => {
      console.error("WebSocket Error:", error);
    };

    socket.onclose = () => {
      console.log("WebSocket Disconnected");
    };

    return () => {
      socket.close();
    };
  }, []);

  useEffect(() => {
    // Fetch backtest data when backtestId is available
    if (backtestId) {
      console.log("backtestId:", backtestId); // Log the backtest ID for debugging purposes
      const fetchBacktestData = async (backtestId: number) => {
        try {
          const response = await axios.get(
            `/api/v1/backtests/results/${backtestId}`
          );
          setBacktestData(response.data);
        } catch (error) {
          console.error("Error fetching backtest data:", error);
        }
      };

      fetchBacktestData(backtestId);
    }
  }, [backtestId]);

  return (
    <div>
      {/* Render BacktestResults only if backtestData is available */}
      <StrategyForm />
      {backtestData ? (
        <BacktestResult backtestData={backtestData} />
      ) : (
        <p>Loading backtest results...</p>
      )}
    </div>
  );
};

export default Backtest;
