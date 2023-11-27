import React, { useEffect, useState } from "react";

interface Params {
  rsi_window: number;
}

interface Result {
  [key: string]: number | string;
  Start: string;
  End: string;
  Duration: string;
  "Exposure Time [%]": number;
  "Equity Final [$]": number;
  "Equity Peak [$]": number;
  "Return [%]": number;
  "Buy & Hold Return [%]": number;
  "Return (Ann.) [%]": number;
  "Volatility (Ann.) [%]": number;
  "Sharpe Ratio": number;
  "Sortino Ratio": number;
  "Calmar Ratio": number;
  "Max. Drawdown [%]": number;
  "Avg. Drawdown [%]": number;
  "Max. Drawdown Duration": string;
  "Avg. Drawdown Duration": string;
  "# Trades": number;
  "Win Rate [%]": number;
  "Best Trade [%]": number;
  "Worst Trade [%]": number;
  "Max. Trade Duration": string;
  "Avg. Trade Duration": string;
  "Profit Factor": number;
  "Expectancy [%]": number;
  SQN: number;
  _strategy: string;
  plot: string;
}

interface BacktestData {
  id: number;
  strategy_name: string;
  symbol: string;
  t_frame: string;
  since: string;
  type: string;
  params: Params;
  plot_url: string;
  details: Result;
}

const BacktestResult: React.FC<{ backtestData: BacktestData }> = ({
  backtestData,
}) => {
  const {
    // id,
    strategy_name,
    symbol,
    t_frame,
    // since,
    // type,
    // params,
    plot_url,
    details,
  } = backtestData;
  const [htmlContent, setHtmlContent] = useState("");

  useEffect(() => {
    const fetchHtmlContent = async () => {
      try {
        const response = await fetch(
          "https://my-trading-bot.s3.ap-northeast-1.amazonaws.com/" + plot_url
        );
        const html = await response.text();
        setHtmlContent(html);
      } catch (error) {
        console.error("Error fetching HTML content:", error);
      }
    };

    fetchHtmlContent();
  }, [backtestData]);

  return (
    <div className="bg-gray-800 text-white p-6 rounded-lg shadow-xl">
      <h2 className="text-2xl font-bold mb-4">
        Backtest Results: {strategy_name}
      </h2>
      <p className="font-bold mb-2">Symbols: {symbol}</p>
      <p className="font-bold mb-2">Time frame: {t_frame}</p>
      <h3 className="text-xl font-bold mb-2">Plot</h3>
      <iframe
        className="w-full h-[600px] border-none"
        srcDoc={htmlContent}
        title="Backtest Plot"
        allowFullScreen
      ></iframe>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-1 my-2">
        {/* Display the result data */}
        {Object.entries(details).map(([key, value]) => {
          // Skip the plot URL for separate handling
          if (key === "plot" || key === "_strategy") return null;
          return (
            <div
              key={key}
              className="bg-gray-700 p-1 rounded flex justify-between items-center"
            >
              <span className="font-medium">{key.replace(/_/g, " ")}</span>
              <span>
                {typeof value === "number" ? value.toFixed(2) : value}
              </span>
            </div>
          );
        })}
      </div>
      <div className="mt-6">
        {/* <button
          onClick={() => goFullScreen()}
          className="mt-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-700"
        >
          Full Screen
        </button> */}
        {/* Embed the plot in an iframe */}
        {/* <iframe
          className="w-full h-96"
          // Use fullUrl as the src for the iframe
          allowFullScreen
          src={info.s3_url?.split("backtest")[0] + result.plot}
          title="Backtest Plot"
        ></iframe> */}
      </div>
    </div>
  );
};

export default BacktestResult;
