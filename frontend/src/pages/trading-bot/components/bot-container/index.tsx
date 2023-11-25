import { useEffect, useState } from "react";
import axios from "axios";
import { Bot } from "../../models";

const BotContainer: React.FC = () => {
  const [bots, setBots] = useState<Bot[]>([]);
  const userId = 1;
  const bot_api_base = `/api/v1/bots/users/${userId}/bots`;
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(bot_api_base);
        const bots = response.data.data
        setBots(bots.filter((bot: Bot) => bot.status == "running"));
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  const handleStop = async (botId: number) => {
    try {
      const resp = await axios.put(`${bot_api_base}/${botId}`);
      console.log(resp.data);
      alert("Stop OK!");
      setBots((prevBots) =>
        prevBots.map((bot) =>
          bot.id === botId ? { ...bot, status: "stopped" } : bot
        )
      );
    } catch (error: any) {
      console.error(error.response.data?.detail);
      alert(
        error.response.data?.detail || "Something went run when stopping bot"
      );
    }
  };

  const handleDelete = async (botId: number) => {
    try {
      const resp = await axios.delete(`${bot_api_base}/${botId}`);
      console.log(resp.data);
      alert("Delete OK!");
      setBots((prevBots) => prevBots.filter((bot) => bot.id !== botId));
    } catch (error: any) {
      console.error(error);
      alert(
        error.response.data?.detail || "Something went wrong when deleting bot"
      );
    }
    const resp = await axios.delete(`${bot_api_base}/${botId}`);
    console.log(resp);

    // Update state or trigger side effects as necessary
  };

  return (
    <div className="flex flex-col gap-6 p-6">
      {bots.map((bot) => (
        <div
          key={bot.id}
          className="bg-gray-800 p-6 rounded-lg shadow-lg flex justify-between items-center text-white"
        >
          <div className="flex flex-col">
            <span className="text-xl font-semibold">{bot.name}</span>
            <span className="text-gray-400">{bot.symbol}</span>
          </div>
          <div className="text-right">
            <div className="text-lg">{bot.strategy}</div>
            {/* <div className="text-gray-400">200 U</div> */}
          </div>
          <div className="text-right">
            <div className="text-lg">總利潤</div>
            <div className="text-gray-400">3.01 U (-10%)</div>
          </div>
          <div className="flex gap-4">
            <button
              className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded inline-flex items-center"
              onClick={() => handleStop(bot.id)}
            >
              {/* <svg
                className="fill-current w-4 h-4 mr-2"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
              >
                <path d="M..." />{" "} */}
              {/* Add an appropriate path data for 'stop' icon */}
              {/* </svg> */}
              <span>Stop</span>
            </button>
            <button
              className="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded inline-flex items-center"
              onClick={() => handleDelete(bot.id)}
            >
              <span>Delete</span>
            </button>
          </div>
          <div
            className={`px-3 py-1 rounded-full text-sm font-semibold ${
              bot.status === "running" ? "bg-green-500" : "bg-red-500"
            }`}
          >
            {bot.status.toUpperCase()}
          </div>
        </div>
      ))}
    </div>
  );
};

export default BotContainer;
