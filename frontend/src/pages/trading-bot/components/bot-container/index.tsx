import React, { useEffect, useState } from "react";
import axios from "axios";
import { Bot, MarkPriceData } from "@/pages/trading-bot/models";
import { useNavigate } from "react-router-dom";
import useCookie from "@/common/hooks/useCookie";
import { user_api_base, bot_api_base } from "@/common/apis";
// import { Label } from "@/components/ui/label";

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Icons } from "@/components/ui/icons";
// import { Icons } from "@/components/ui/icons";

const BotContainer: React.FC = () => {
  const [bots, setBots] = useState<Bot[]>([]); // const userId = 1;
  const [loadingStates, setLoadingStates] = useState<{ [key: number]: boolean }>({});
  const [markAllPrice, setMarkAllPrice] = useState<MarkPriceData[] | null>(
    null
  );
  // const { userId } = useParams<{ userId: string }>();
  const [userId] = useCookie("user_id", "");
  // const [isLoading, setIsLoading] = React.useState<boolean>(false);

  // const { markPrice } = useContext(TradingDataContext);
  const user_api = user_api_base(userId);
  const navigate = useNavigate();

  const handleBotClick = (botId: number) => {
    navigate(`/trading-bots/${botId}`);
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
        const response = await axios.get(`${user_api}/bots`);
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
      if (confirm(`確定要終止機器人嗎 ?`)) {
        setLoadingStates(prevStates => ({ ...prevStates, [botId]: true })); // Start loading for specific bot
        const resp = await axios.put(`${bot_api_base(botId)}`);
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
    } finally {
      setLoadingStates(prevStates => ({ ...prevStates, [botId]: false })); // Stop loading for specific bot
    }
  };

  const handleDelete = async (event: any, botId: number) => {
    try {
      event.preventDefault();
      if (confirm("確定要刪除機器人嗎 ?") && botId) {
        const resp = await axios.delete(`${bot_api_base(botId)}`);
        console.log(resp.data);
        alert("Delete OK!");
        setBots((prevBots) => prevBots.filter((bot) => bot.id !== botId));
      } else return;
    } catch (error: any) {
      console.error(error);
      alert(
        error.response.data?.detail || "Something went wrong when deleting bot"
      );
    }
  };

  const calculateTotalPnl = (bot: Bot): number => {
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

    return +(totalUnrealizedPnl + totalRealizedPnl).toFixed(3) || 0;
  };

  return (
    <>
      <div className="flex flex-wrap gap-5 p-6 text-slate-200">
        {bots.length === 0 || !bots ? (
          // <h1>尚無機器人，快來新增一個看看吧！</h1>
          <></>
        ) : (
          bots.map((bot, i) => (
            <Card
              key={i}
              className="flex flex-col flex-wrap min-h-[250px] md:h-[280px] bg-zinc-900 justify-between rounded-lg border-0 text-slate-200 w-full md:w-1/2 md:max-w-[450px]"
              // style={{ backgroundColor: "#222831" }}
            >
              <CardHeader className="flex flex-col">
                <CardTitle className=" flex flex-wrap justify-between tracking-wide gap-1">
                  {/* 可能要限制一下字數要不然會很醜  */}
                  <p className="text-2xl md:tracking-widest break-all ">
                    {bot.name}
                  </p>
                  <div
                    className={`px-3 py-1 rounded-full text-sm font-semibold w-[100px] text-center
                  ${bot.status === "running" ? "bg-green-800" : "bg-red-900"}`}
                  >
                    {bot.status.toUpperCase()}
                  </div>
                </CardTitle>
                <CardDescription className="flex gap-3">
                  <p className="text-gray-300">{bot.symbol}</p>
                  <p className="text-gray-300">{bot.strategy} 策略</p>
                </CardDescription>
              </CardHeader>
              <CardContent className="text-gray-300">
                <div className="flex gap-5 text-lg">
                  <p className="">
                    浮動利潤 <span className="text-[10px]">USDT</span>
                  </p>
                  <strong
                    className={`${
                      calculateTotalPnl(bot) < 0
                        ? "text-pink-600"
                        : "text-white"
                    }`}
                  >
                    {calculateTotalPnl(bot)}
                  </strong>
                </div>
              </CardContent>

              <CardFooter className="flex gap-3 md:gap-5 ">
                {bot.status === "running" ? (
                  <Button
                    className="w-1/2 hover:bg-red-900"
                    onClick={(event) => handleStop(event, bot.id)}
                    disabled={bot.status !== "running" || loadingStates[bot.id]}
                    >
                    <span>
                      {loadingStates[bot.id] && (
                        <Icons.spinner className="mr-2 h-4 w-4 animate-spin" />
                      )}
                      
                    </span>終止
                  </Button>
                ) : (
                  <Button
                    className="w-1/2  hover:bg-blue-900"
                    onClick={(event) => handleDelete(event, bot.id)}
                  >
                    <span>移除</span>
                  </Button>
                )}
                <Button
                  // disabled={isLoading}
                  onClick={() => handleBotClick(bot.id)}
                  className="w-1/2 hover:bg-zinc-700"
                >
                  {/* {isLoading && (
                  <Icons.spinner className="mr-2 h-4 w-4 animate-spin" />
                )} */}
                  詳情
                </Button>
              </CardFooter>
            </Card>
          ))
        )}
      </div>
    </>
  );
};

export default BotContainer;
