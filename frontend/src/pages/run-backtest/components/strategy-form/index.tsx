import axios from "axios";
import React, { useState } from "react";

const StrategyForm = () => {
  const bot_api_base = `/api/v1/backtests`;
  const [strategy, setStrategy] = useState({
    name: "MaRSI",
    symbols: ["BTC/USDT"], // TODO fix this (use string not list)
    t_frame: "1h",
    since: "2023-01-01",
    default_type: "future",
    params: {
      rsi_window: 20,
    },
  });

  const handleInputChange = (event: any) => {
    const { name, value } = event.target;
    if (name === "symbols") {
      setStrategy({ ...strategy, [name]: [value] }); // Handle symbols as an array
    } else {
      setStrategy({ ...strategy, [name]: value });
    }
  };

  const handleParamChange = (event: any) => {
    const { name, value } = event.target;
    setStrategy({
      ...strategy,
      params: { ...strategy.params, [name]: Number(value) },
    });
  };

  const handleSubmit = async (event: any) => {
    event.preventDefault();
    console.log("Submitting Strategy", strategy);

    try {
      const isoDateString = new Date(strategy.since).toISOString();

      const submissionData = {
        ...strategy,
        since: isoDateString, // Use the ISO string format
      };
      const resp: any = await axios.post(bot_api_base, submissionData);
      console.log(resp.data.message);
      alert("Start running backtest");
    } catch (error: any) {
      console.error(error.response.data);
      alert(
        error.response.data?.message ||
          "Something went wrong when submitting backtest"
      );
    }
    // Add code to submit data to the server
  };

  return (
    <div className="max-w-lg mx-auto my-10 p-6 bg-gray-800 text-white rounded-lg shadow-xl">
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-sm font-medium mb-2">Strategy:</label>
          <select
            name="name"
            value={strategy.name}
            onChange={handleInputChange}
            className="w-full p-2 rounded bg-gray-700 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          >
            <option value="MaRSI">MaRSI</option>
            <option value="MaCrossover">MaCrossover</option>
            <option value="SuperTrend">SuperTrend</option>
            <option value="RsiOscillator">RsiOscillator</option>
          </select>
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium mb-2">Symbols:</label>
          <select
            name="symbols"
            value={strategy.symbols}
            onChange={handleInputChange}
            className="w-full p-2 rounded bg-gray-700 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          >
            <option value="BTC/USDT">BTC/USDT</option>
            <option value="ETH/USDT">ETH/USDT</option>
            <option value="XRP/USDT">XRP/USDT</option>
          </select>
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium mb-2">Time Frame:</label>
          <select
            name="t_frame"
            value={strategy.t_frame}
            onChange={handleInputChange}
            className="w-full p-2 rounded bg-gray-700 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          >
            <option value="1d">1 day</option>
            <option value="4h">4 hours</option>
            <option value="1h">1 hour</option>
          </select>
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium mb-2">Since:</label>
          <input
            type="date"
            name="since"
            value={strategy.since}
            onChange={handleInputChange}
            className="w-full p-2 rounded bg-gray-700 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        <div className="mb-6">
          <label className="block text-sm font-medium mb-2">RSI Window:</label>
          <input
            type="number"
            name="rsi_window"
            value={strategy.params.rsi_window}
            onChange={handleParamChange}
            className="w-full p-2 rounded bg-gray-700 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        <div className="flex justify-end">
          <button
            type="submit"
            className="px-6 py-2 rounded bg-blue-500 hover:bg-blue-700 transition-colors duration-300 ease-in-out"
          >
            Go
          </button>
        </div>
      </form>
    </div>
  );
};

export default StrategyForm;
