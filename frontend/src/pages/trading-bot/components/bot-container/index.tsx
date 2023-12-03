import { useEffect, useState } from "react";
import axios from "axios";
import { Bot, MarkPriceData } from "../../models";
import { useNavigate, useParams } from "react-router-dom";

const BotContainer: React.FC = () => {
  const [bots, setBots] = useState<Bot[]>([]); // const userId = 1;
  const [markAllPrice, setMarkAllPrice] = useState<MarkPriceData[] | null>(
    null
  );
  const { userId } = useParams<{ userId: string }>();
  // const { markPrice } = useContext(TradingDataContext);
  const bot_api_base = `/api/v1/bots/users/${userId}/bots`;
  const navigate = useNavigate();

  const handleBotClick = (botId: number) => {
    navigate(`/user/${userId}/trading-bots/${botId}`);
  };

  useEffect(() => {
    // Initialize WebSocket connections
    const markPriceWs = new WebSocket(
      "wss://fstream.binance.com/ws/!markPrice@arr@1s"
    );

    markPriceWs.onmessage = (event) => {
      const message: MarkPriceData[] = JSON.parse(event.data);
      console.log("Hi from binance ws", message[0]);
      setMarkAllPrice(message);
    };

    // Clean up function
    return () => {
      markPriceWs.close();
    };
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(bot_api_base);
        const bots = response.data.data;
        setBots(bots.filter((bot: Bot) => bot.status !== "deleted"));
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);


  const handleStop = async (event: any, botId: number) => {
    try {
      event.stopPropagation();
      if (confirm(`Sure to stop bot ${botId} ?`)) {
        const resp = await axios.put(`${bot_api_base}/${botId}`);
        console.log(resp.data);
        alert("Stop OK!");

        setBots((prevBots) =>
          prevBots.map((bot) =>
            bot.id === botId ? { ...bot, status: "stopped" } : bot
          )
        );
      }
    } catch (error: any) {
      console.error(error.response.data?.detail);
      alert(
        error.response.data?.detail || "Something went run when stopping bot"
      );
    }
  };

  const handleDelete = async (event: any, botId: number) => {
    try {
      event.preventDefault();
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
  };

  const calculateTotalPnl = (bot: Bot) => {
    let totalRealizedPnl = bot.trade_history.reduce(
      (sum, trade) => sum + (trade.realizedPnl || 0),
      0
    );
    let length = bot.trade_history.length;
    let totalUnrealizedPnl = 0;
    if (length % 2 !== 0) {
      // having open position
      let lastTrade = bot.trade_history[length - 1];
      let markPrice = markAllPrice
        ?.filter((price) => price.s === lastTrade.info.symbol)
        .map((symbol) => symbol.p);
      totalUnrealizedPnl =
        (Number(markPrice?.[0]) - lastTrade.avg_price) * lastTrade.qty;
    }

    return (totalUnrealizedPnl + totalRealizedPnl).toFixed(3);
  };

  return (
    <>
      {/* <BinancePrices /> */}
      <div className="flex flex-col gap-6 p-6">
        {bots.map((bot) => (
          <div
            key={bot.id}
            className="bg-gray-800 p-6 rounded-lg shadow-lg flex justify-between items-center text-white"
          >
            <div
              className="flex flex-col"
              onClick={() => handleBotClick(bot.id)}
            >
              <span className="text-xl font-semibold">{bot.name}</span>
              <span className="text-gray-400">{bot.symbol}</span>
            </div>
            <div className="text-right">
              <div className="text-lg">{bot.strategy}</div>
              {/* <div className="text-gray-400">200 U</div> */}
            </div>
            <div className="text-right">
              <div className="text-lg">浮動利潤</div>
              {/* <div className="text-gray-400">3.01 U (-10%)</div> */}
              <div className="text-gray-400">{calculateTotalPnl(bot)} U</div>
            </div>
            <div className="flex gap-4">
              <button
                className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded inline-flex items-center"
                onClick={(event) => handleStop(event, bot.id)}
              >
                <span>Stop</span>
              </button>
              <button
                className="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded inline-flex items-center"
                onClick={(event) => handleDelete(event, bot.id)}
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
    </>
  );
};

export default BotContainer;
