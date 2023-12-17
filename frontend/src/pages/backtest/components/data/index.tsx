import React, { useEffect, useState } from "react";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

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
    since,
    // type,
    // params,
    plot_url,
    details,
  } = backtestData;
  const [htmlContent, setHtmlContent] = useState("");

  const tableData = {
    Trades: details["# Trades"],
    Return: details["Return [%]"],
    "BuyHold Return": details["Buy & Hold Return [%]"],
    "Win Rate": details["Win Rate [%]"],
    "Profit Factor": details["Profit Factor"],
    "Avg Drawdown": details["Avg. Drawdown [%]"],
    "Max Drawdown": details["Max. Drawdown [%]"],
    Volatility: details["Volatility (Ann.) [%]"],
    "Calmar Ratio": details["Calmar Ratio"],
    "Sharpe Ratio": details["Sharpe Ratio"],
    "Sortino Ratio": details["Sortino Ratio"],
  };

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

  function isFloat(n: any) {
    return Number(n) === n && n % 1 !== 0;
  }

  return (
    <div className="text-white p-6 flex flex-col gap-5">
      {/* <h2 className="text-2xl font-bold mb-4">
        Backtest Results: {strategy_name}
      </h2> */}
      <div className="flex gap-5 ml-5">
        <p className="font-bold text-slate-300"> {strategy_name} </p>
        <p className="font-bold text-slate-300"> {symbol} </p>
        <p className="font-bold text-slate-300"> {t_frame} </p>
        <p className="font-bold text-slate-300"> {since.split('T')[0]} ~ Now</p>
      </div>

      <iframe
        className="w-full h-[700px] border-none"
        srcDoc={htmlContent}
        title="Backtest Plot"
        allowFullScreen
      ></iframe>
      <Table>
        <TableCaption></TableCaption>
        <TableHeader>
          <TableRow>
            {Object.keys(tableData).map((key) => (
              <TableCell key={key} className="p-1 py-5 text-center bg-zinc-800">
                {key}
              </TableCell>
            ))}
          </TableRow>
        </TableHeader>

        <TableBody></TableBody>
        <TableRow>
          {Object.values(tableData).map((value, index) => (
            <TableCell key={index} className="py-5 text-center">
              {isFloat(value) ? value.toFixed(2) : value || "N/A"}
            </TableCell>
          ))}
        </TableRow>
      </Table>
    </div>
  );
};

export default BacktestResult;
