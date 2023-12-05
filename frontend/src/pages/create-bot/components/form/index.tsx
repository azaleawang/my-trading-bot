import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { bot_api_base } from "@/common/apis";
import useCookie from "@/common/hooks/useCookie";
import { Button } from "@/components/ui/button";

const CreateBotForm: React.FC = () => {
  
  const navigate = useNavigate();
  const [userId] = useCookie("user_id", "");
  const [botData, setBotData] = useState({
    name: "",
    strategy: "supertrend",
    symbol: "",
    description: "",
    t_frame: "30m",
    quantity: 120
  });
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
      owner_id: Number(userId),
      created_at: new Date().toISOString(),
    };
    try {
      console.log(submissionData);
      const response = await axios.post(
        `${bot_api_base(undefined)}/`,
        submissionData
      );
      console.log(response.data);
      if (
        confirm(
          `Bot ${response.data.data.name} created successfully! 交易對: ${response.data.data.symbol}`
        )
      ) {
        navigate(`/trading-bots`);
      }

      // Handle the success (e.g., showing a notification, clearing the form, etc.)
    } catch (error: any) {
      console.error("Error creating bot:", error);
      alert(
        error.response?.data?.detail || "Something went wrong when creating bot"
      );
      // Handle the error (e.g., showing an error message)
    }
  };

  return (
    <div className="w-10/12 max-w-[500px] p-5 m-auto text-white">
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="name" className="block text-base font-medium mb-2">
            機器人命名
          </label>
          <input
            type="text"
            id="name"
            name="name"
            value={botData.name}
            onChange={handleInputChange}
            placeholder="請用英文輸入"
            className="w-full p-2 rounded bg-zinc-700 focus:outline-none focus:ring-2 focus:ring-zinc-500"
            required
          />
        </div>
        <div className="mb-4">
          <label htmlFor="strategy" className="block text-base font-medium mb-2">
            運行策略
          </label>
          <select
            id="strategy"
            name="strategy"
            value={botData.strategy}
            onChange={handleInputChange}
            className="w-full p-2 rounded bg-zinc-700 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-zinc-500"
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
          <label htmlFor="symbol" className="block text-base font-medium mb-2">
            交易對
          </label>
          <select
            id="symbol"
            name="symbol"
            value={botData.symbol}
            onChange={handleInputChange}
            className="w-full p-2 rounded bg-zinc-700 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-zinc-500"
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
        {/* <div className="mb-4">
          <label className="block text-base font-medium mb-2">策略運行時框</label>
          <select
            name="t_frame"
            value={botData.t_frame}
            onChange={handleInputChange}
            className="w-full p-2 rounded bg-zinc-700 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-zinc-500"
            required
          >
            <option value="1d">1 day</option>
            <option value="4h">4 hours</option>
            <option value="1h">1 hour</option>
            <option value="30m">30 mins</option>
          </select>
        </div> */}
        <div className="mb-4">
          {/* <Slider defaultValue={[33]} max={100} step={1} /> */}

          <label htmlFor="quantity" className="block text-base font-medium mb-2">
            每次買入 (USDT)
          </label>
          <input
            type="number"
            id="quantity"
            name="quantity"
            value={botData.quantity}
            onChange={handleInputChange}
            className="w-full p-2 rounded bg-zinc-700 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-zinc-500"
            min="11"
            max="500"
            required
          />
        </div>
        {/* <div className="mb-6">
          <label
            htmlFor="description"
            className="block text-base font-medium mb-2"
          >
            Description (Optional)
          </label>
          <textarea
            id="description"
            name="description"
            value={botData.description}
            onChange={handleInputChange}
            className="w-full p-2 rounded bg-zinc-700 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-zinc-500"
            rows={4}
          ></textarea>
        </div> */}
        <div className="flex justify-end">
          <Button
            type="submit"
          >
            Create Bot
          </Button>
        </div>
      </form>
    </div>
  );
};

export default CreateBotForm;
