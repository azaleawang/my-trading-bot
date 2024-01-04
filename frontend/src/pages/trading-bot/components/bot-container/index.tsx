import React, { useEffect, useState } from "react";
import axios from "axios";
import { Bot, MarkPriceData } from "@/pages/trading-bot/models";
import { useNavigate } from "react-router-dom";
import useCookie from "@/common/hooks/useCookie";
import { user_api_base, bot_api_base } from "@/common/apis";
import { Player } from "@lottiefiles/react-lottie-player";

import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Icons } from "@/components/ui/icons";
import CreateBotForm from "@/pages/create-bot/components/form";
import { toast } from "react-toastify";
const BotContainer: React.FC = () => {
  const [access_token] = useCookie("access_token", "");
  const [bots, setBots] = useState<Bot[]>([]);
  const [loadingStates, setLoadingStates] = useState<{
    [key: number]: boolean;
  }>({});
  const [markAllPrice, setMarkAllPrice] = useState<MarkPriceData[] | null>(
    null
  );
  const [userId] = useCookie("user_id", "");

  const user_api = user_api_base(userId);
  const navigate = useNavigate();
  const [botLoading, setBotLoading] = useState<boolean>(true);
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
        const response = await axios.get(`${user_api}/bots`, {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        });
        const bots = response.data.data;
        setBots(bots?.filter((bot: Bot) => bot.status !== "deleted"));
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setBotLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleStop = async (event: any, botId: number) => {
    try {
      event.stopPropagation();
      if (confirm(`確定要終止機器人嗎 ?`)) {
        setLoadingStates((prevStates) => ({ ...prevStates, [botId]: true })); // Start loading for specific bot
        const resp = await axios.put(
          `${bot_api_base(botId)}`,
          {},
          {
            headers: {
              Authorization: `Bearer ${access_token}`,
            },
          }
        );
        console.log(resp.data);
        toast.success("成功終止機器人", {
          autoClose: 1000,
        });

        setBots((prevBots) =>
          prevBots.map((bot) =>
            bot.id === botId ? { ...bot, status: "stopped" } : bot
          )
        );
      }
    } catch (error: any) {
      console.error(error.response.data?.detail);
      toast.error(
        error.response.data?.detail || "Something went run when stopping bot"
      );
    } finally {
      setLoadingStates((prevStates) => ({ ...prevStates, [botId]: false })); // Stop loading for specific bot
    }
  };

  const handleDelete = async (event: any, botId: number) => {
    try {
      event.preventDefault();
      if (confirm("確定要刪除機器人嗎 ?") && botId) {
        const resp = await axios.delete(`${bot_api_base(botId)}`, {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        });
        console.log(resp.data);
        toast.success("移除成功", {
          autoClose: 1000,
        });
        setBots((prevBots) => prevBots.filter((bot) => bot.id !== botId));
      } else return;
    } catch (error: any) {
      console.error(error);
      toast.error(
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

  if (botLoading) {
    return (
      <div className="text-xl text-slate-400 flex justify-center h-[300px]">
        {/* <Icons.spinner className="mr-5 h-[100px] w-[100px] animate-spin" />
        <span>Loading...</span> */}
      </div>
    );
  }

  return (
    <div className="flex flex-col justify-between">
      <div className="flex flex-wrap gap-5 p-6 text-slate-200 mt-10">
        {bots?.length == 0 ? (
          <div className="flex flex-col gap-5 mt-5 w-full">
            <Player
              autoplay
              loop
              src="https://lottie.host/5debc6b1-ed25-493f-8ec6-1951aea44469/KXcHRm0dhd.json"
              style={{ height: "150px", width: "150px" }}
            ></Player>
            <h1 className="mt-5 m-auto">尚無機器人，快來新增一個看看吧！</h1>
            <div className="inline-flex items-center justify-center whitespace-nowrap rounded-md text-base p-0 h-[35px] w-[150px] m-auto bg-orange-300/60 hover:bg-orange-300/50">
              <CreateBotForm />
            </div>
          </div>
        ) : (
          <>
            <div className=" flex fixed right-0 top-20">
              <div className="inline-flex items-center justify-center whitespace-nowrap rounded-md text-base p-0 h-[35px] mr-5 w-[100px] p-0 bg-inherit border-2 border-zinc-300 hover:bg-black">
                <CreateBotForm />
              </div>
            </div>
            {bots.map((bot, i) => (
              <Card
                key={i}
                className="flex flex-col flex-wrap min-h-[250px] md:h-[280px] bg-zinc-900 justify-between rounded-lg border-0 text-slate-200 w-full md:w-1/2 md:max-w-[450px]"
              >
                <CardHeader className="flex flex-col">
                  <CardTitle className=" flex flex-wrap justify-between tracking-wide gap-1">
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
                  <div className="flex gap-3">
                    <p className="text-gray-300">{bot.symbol}</p>
                    <p className="text-gray-300">{bot.strategy} 策略</p>
                  </div>
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
                      disabled={
                        bot.status !== "running" || loadingStates[bot.id]
                      }
                    >
                      <span>
                        {loadingStates[bot.id] && (
                          <Icons.spinner className="mr-2 h-4 w-4 animate-spin" />
                        )}
                      </span>
                      終止
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
            ))}
          </>
        )}
      </div>
    </div>
  );
};

export default BotContainer;
