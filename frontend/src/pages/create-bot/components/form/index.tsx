import React, { useState } from "react";
import axios from "axios";
import { useNavigate, useParams } from "react-router-dom";

const CreateBotForm: React.FC = () => {
  const [botData, setBotData] = useState({
    name: "",
    strategy: "",
    symbol: "",
    description: "",
    t_frame: "30m",
    quantity: 120
  });
  const navigate = useNavigate();
  const { userId } = useParams<{ userId: string }>();
  const strategies = ["supertrend"]; // only accept this strategy for now
  const symbols = ["ETH/USDT", "BTC/USDT", "BNB/USDT"]; // still hard-coded

  const handleInputChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
    >
  ) => {
    setBotData({ ...botData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const submissionData = {
      ...botData,
      created_at: new Date().toISOString(),
    };
    try {
      // Replace with your actual API endpoint
      const response = await axios.post(
        `/api/v1/bots/users/${userId}/bots`,
        submissionData
      );
      console.log(response.data);
      if (confirm(`Bot ${response.data.data.name} created successfully! 交易對: ${response.data.data.symbol}`)) {
        navigate(`/user/${userId}/trading-bots`);
      }

      // Handle the success (e.g., showing a notification, clearing the form, etc.)
    } catch (error: any) {
      console.error("Error creating bot:", error);
      alert(error.response?.data?.detail || "Something went wrong when creating bot")
      // Handle the error (e.g., showing an error message)
    }
  };

  return (
    <div className="max-w-lg mx-auto my-10 p-6 bg-gray-800 text-white rounded-lg shadow-xl">
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="name" className="block text-sm font-medium mb-2">
            Bot Name
          </label>
          <input
            type="text"
            id="name"
            name="name"
            value={botData.name}
            onChange={handleInputChange}
            className="w-full p-2 rounded bg-gray-700 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        <div className="mb-4">
          <label htmlFor="strategy" className="block text-sm font-medium mb-2">
            Strategy
          </label>
          <select
            id="strategy"
            name="strategy"
            value={botData.strategy}
            onChange={handleInputChange}
            className="w-full p-2 rounded bg-gray-700 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          >
            <option value="">Select a strategy</option>
            {strategies.map((strategy) => (
              <option key={strategy} value={strategy}>
                {strategy}
              </option>
            ))}
          </select>
        </div>
        <div className="mb-4">
          <label htmlFor="symbol" className="block text-sm font-medium mb-2">
            Trading Pair
          </label>
          <select
            id="symbol"
            name="symbol"
            value={botData.symbol}
            onChange={handleInputChange}
            className="w-full p-2 rounded bg-gray-700 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          >
            <option value="">Select a trading pair</option>
            {symbols.map((symbol) => (
              <option key={symbol} value={symbol}>
                {symbol}
              </option>
            ))}
          </select>
        </div>
        <div className="mb-4">
          <label className="block text-sm font-medium mb-2">Time Frame:</label>
          <select
            name="t_frame"
            value={botData.t_frame}
            onChange={handleInputChange}
            className="w-full p-2 rounded bg-gray-700 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          >
            <option value="1d">1 day</option>
            <option value="4h">4 hours</option>
            <option value="1h">1 hour</option>
            <option value="30m">30 mins</option>
          </select>
        </div>
        <div className="mb-4">
          <label htmlFor="quantity" className="block text-sm font-medium mb-2">
            Quantity (USDT)
          </label>
          <input
            type="number"
            id="quantity"
            name="quantity"
            value={botData.quantity}
            onChange={handleInputChange}
            className="w-full p-2 rounded bg-gray-700 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        <div className="mb-6">
          <label
            htmlFor="description"
            className="block text-sm font-medium mb-2"
          >
            Description (Optional)
          </label>
          <textarea
            id="description"
            name="description"
            value={botData.description}
            onChange={handleInputChange}
            className="w-full p-2 rounded bg-gray-700 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={4}
          ></textarea>
        </div>
        <div className="flex justify-end">
          <button
            type="submit"
            className="px-6 py-2 rounded bg-blue-600 hover:bg-blue-700 transition-colors duration-300 ease-in-out"
          >
            Create Bot
          </button>
        </div>
      </form>
    </div>
  );
};

export default CreateBotForm;
