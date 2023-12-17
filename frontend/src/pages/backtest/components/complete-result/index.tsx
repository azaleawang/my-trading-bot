import { useState, useEffect } from "react";
import axios from "axios";
import BacktestResult from "../data";
import StrategyForm from "../strategy-form";
import { Icons } from "@/components/ui/icons";
import useCookie from "@/common/hooks/useCookie";

const Backtest = () => {
  // const [backtestData, setBacktestData] = useState({
  // id: 1,
  // strategy_name: "MaRsi",
  // t_frame: "4h",
  // type: "future",
  // params: {
  //   rsi_window: 20,
  // },
  // created_at: "2023-11-28T21:03:15.408635+08:00",
  // since: "2023-01-01T00:00:00",
  // symbol: "BTC/USDT",
  // plot_url: "backtest/result/SuperTrend_BTC-USDT_1d_20231213-044348.html",
  // details: {
  //   End: "2023-11-28 08:00:00",
  //   SQN: 0.9453312864480757,
  //   plot: "backtest/result/MaRsi_BTC-USDT_1h_20231128-082333.html",
  //   Start: "2023-01-01 00:00:00",
  //   "# Trades": 2,
  //   Duration: "331 days 08:00:00",
  //   _strategy: "MaRsi(params=)",
  //   "Return [%]": 35.532482879999996,
  //   "Calmar Ratio": 1.8197071583421327,
  //   "Sharpe Ratio": 0.6924207896486616,
  //   "Win Rate [%]": 50,
  //   "Profit Factor": null,
  //   "Sortino Ratio": 1.6752137367792543,
  //   "Best Trade [%]": 36.58727154426143,
  //   "Expectancy [%]": 17.911810543827063,
  //   "Equity Peak [$]": 1517576.6848,
  //   "Worst Trade [%]": -0.763650456607301,
  //   "Equity Final [$]": 1355324.8288,
  //   "Avg. Drawdown [%]": -3.649393432304394,
  //   "Exposure Time [%]": 82.08223311957752,
  //   "Max. Drawdown [%]": -21.811709480542106,
  //   "Return (Ann.) [%]": 39.69092387742143,
  //   "Avg. Trade Duration": "135 days 23:00:00",
  //   "Max. Trade Duration": "270 days 20:00:00",
  //   "Buy & Hold Return [%]": 124.00617171900525,
  //   "Volatility (Ann.) [%]": 57.32197021057216,
  //   "Avg. Drawdown Duration": "8 days 05:00:00",
  //   "Max. Drawdown Duration": "137 days 13:00:00",
  // },
  // updated_at: "2023-11-28T21:04:34.076388+08:00",
  // });
  const [backtestData, setBacktestData] = useState();
  const [backtestId, setBacktestId] = useState();
  const [loading, setLoading] = useState<boolean>(false);
  const [userId] = useCookie("user_id", "");
  
  useEffect(() => {
    const socket = new WebSocket(
      `${import.meta.env.VITE_WS_HOST}/ws/backtest_result/${userId}`
    );

    socket.onopen = () => {
      console.log("WebSocket Connected");
    };

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log("Parsed data:", data);
        if (data.id === backtestId) {
          setLoading(false);
          fetchBacktestData(data.id);
        }
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

  // TODO 如果重複兩次一次的 第二次會因為backtestid一樣導致不會更新loading狀態而一直轉圈圈
  const fetchBacktestData = async (backtestId: number) => {
    try {
      const response = await axios.get(
        `/api/v1/backtests/results/${backtestId}`
      );
      setBacktestData(response.data);
    } catch (error) {
      console.error("Error fetching backtest data:", error);
      setBacktestData(undefined);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Fetch backtest data when backtestId is available
    if (backtestId) {
      console.log("backtestId:", backtestId); // Log the backtest ID for debugging purposes

      fetchBacktestData(backtestId);
    }
  }, [backtestId]);

  return (
    <div>
      {/* Render BacktestResults only if backtestData is available */}
      <StrategyForm loading={loading} setLoading={setLoading} />

      <div className="mt-5">
        {loading ? (
          <div className="text-xl text-slate-400 flex justify-center items-center h-[300px]">
            <Icons.spinner className="mr-5 h-[30px] w-[30px] animate-spin" />
            <span>Loading...</span>
          </div>
        ) : backtestData ? (
          <BacktestResult backtestData={backtestData} />
        ) : (
          <h1 className="text-xl text-slate-300 text-center p-5"></h1>
        )}
      </div>
    </div>
  );
};

export default Backtest;
