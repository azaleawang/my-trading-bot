import axios from "axios";
import React, { useEffect, useState, useContext } from "react";
import { useParams } from "react-router-dom";
import { TradingDataContext } from "@/common/hooks/TradingDataContext";
import { BotError, ContainerStateProps } from "../../models";
import { bot_api_base } from "@/common/apis";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

const BotDetails: React.FC = () => {
  const { botId } = useParams<{ botId: string }>();
  const bot_api = bot_api_base(botId);
  const { botData, setBotData } = useContext(TradingDataContext);
  const [botErrors, setBotErrors] = useState<BotError[]>([]);
  const [containerData, setContainerData] = useState<
    ContainerStateProps | undefined
  >();
  useEffect(() => {
    const fetchBotDetails = async () => {
      try {
        // Replace with your actual API endpoint
        const response = await axios.get(`${bot_api}/trade-history`);
        setBotData(response.data?.data);
        console.log("fetching data", response.data?.data);
      } catch (error) {
        console.error("Error fetching bot details:", error);
        // Handle error appropriately
      }
    };

    if (botId) {
      fetchBotDetails();
    }
  }, [botId]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(`${bot_api}/bot-error`);
        setBotErrors(response.data);
        console.log("Bot errors:", response.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, [botId]);

  useEffect(() => {
    const fetchContainerData = async () => {
      try {
        // TODO 這樣一直重複打資料庫真的好嘛？外面已經撈過全部的資料了
        const response = await axios.get(`${bot_api}/container-monitoring`);
        if (response.data.data[0]) {
          setContainerData(response.data.data[0]);
          console.log("set ContainerData:", response.data.data[0]);
        } else {
          console.log("No container data found");
        }
      } catch (error) {
        console.error("Error fetching container data:", error);
      }
    };

    fetchContainerData();
  }, [botId]);
  // Format the timestamp
  const formattedTimestamp = (timestamp: number) =>
    new Date(timestamp).toLocaleString("zh-TW", {
      hour12: false,
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });

  // Format isoString
  const formatIOString = (isoString: string) => {
    const date = new Date(isoString);
    const offsetHours = 8;
    date.setHours(date.getHours() + offsetHours);

    const formatted = date.toISOString().replace("T", " ").slice(0, 19);

    return formatted;
  };
  return (
    <div className="p-5 flex md:gap-5 flex-wrap text-slate-200 ">
      {/* Left panel: History */}
      <div className="flex flex-col w-full md:w-1/2 md:max-w-xl p-0">
        <Accordion type="single" collapsible>
          <AccordionItem value="history-trade">
            <AccordionTrigger>歷史成交</AccordionTrigger>

            {botData && botData.length > 0 ? (
              <>
                {botData.map((bot, i) => (
                  <AccordionContent key={bot.id} className="">
                    <Card
                      key={i}
                      className="bg-stone-800 text-white px-1 rounded-lg shadow-lg my-5 mx-3 border-stone-500 border-0 rounded-none border-b-2"
                    >
                      <CardHeader className="flex">
                        <div className="flex justify-between flex-wrap">
                          <CardTitle>{bot.info.symbol} 永續</CardTitle>
                          <div className="text-gray-300 text-xs">
                            {formattedTimestamp(bot.timestamp)}
                          </div>
                        </div>

                        <CardDescription className="flex justify-between flex-wrap">
                          <p
                            className={` text-base font-bold
                        ${
                          bot.info.side === "BUY"
                            ? "text-green-500"
                            : "text-red-500"
                        }`}
                          >
                            {bot.info.side}
                          </p>
                          <p className="text-gray-300 text-xs">
                            # {bot.order_id}
                          </p>
                        </CardDescription>
                      </CardHeader>
                      <CardContent className="text-gray-300">
                        <div className="flex justify-between">
                          <p>價格</p>
                          <p> {bot.avg_price.toFixed(2)}</p>
                        </div>
                        <div className="flex justify-between">
                          <p>成交量</p>
                          <p> {bot.qty}</p>
                        </div>
                        <div className="flex justify-between">
                          <p>成交額 (USDT)</p>
                          <p> {Number(bot.info.cumQuote).toFixed(2)}</p>
                        </div>
                        <div className="flex justify-between">
                          <p>已實現盈虧</p>
                          <p> {bot.realizedPnl || 0.0}</p>
                        </div>
                      </CardContent>

                      <CardFooter className="text-gray-300 text-sm">
                        <p>{bot.action === "test" ? "* 測試 *" : ""}</p>
                      </CardFooter>
                    </Card>
                  </AccordionContent>
                ))}
              </>
            ) : (
              <AccordionContent>尚無交易記錄哦!</AccordionContent>
            )}
          </AccordionItem>
        </Accordion>
      </div>

      {/* Right panel: Other details */}
      <div className="flex flex-col grow"> 
      {/* basis-7/12 sm:basis-ful */}
        <Accordion type="single" collapsible>
          <AccordionItem value="trade-error">
            <AccordionTrigger>
              交易執行錯誤: 發現{botErrors.length}個
            </AccordionTrigger>

            {botErrors.length === 0 ? (
              <AccordionContent>讚讚 目前交易所沒有回報錯誤</AccordionContent>
            ) : (
              botErrors.map((error, index) => (
                <AccordionContent key={index}>
                  <p>{new Date(error.timestamp).toLocaleString()}</p>
                  <p>{error.error}</p>
                </AccordionContent>
              ))
            )}
          </AccordionItem>
        </Accordion>
        <Accordion type="single" collapsible>
          <AccordionItem value="container-status">
            <AccordionTrigger>
              機器運作狀態: {containerData?.state.toUpperCase() || "Unknown"}
            </AccordionTrigger>
            <AccordionContent>
              <p>容器名稱: {containerData?.container_name || "Unknown"}</p>
            </AccordionContent>
            <AccordionContent>
              <p>運作時間: {containerData?.running_for || "Unknown"}</p>
            </AccordionContent>
            <AccordionContent>
              <p>
                上次更新:{" "}
                {containerData?.updated_at
                  ? formatIOString(containerData.updated_at)
                  : "Unknown"}
              </p>
            </AccordionContent>
          </AccordionItem>
        </Accordion>
        <Accordion type="single" collapsible>
          <AccordionItem value="container-status">
            <AccordionTrigger>最新 5 筆 Logs (UTC+8)</AccordionTrigger>

            {containerData?.logs.map((log, i) => (
              <AccordionContent key={i}>{log}</AccordionContent>
            )) || "Unknown"}
          </AccordionItem>
        </Accordion>
      </div>
    </div>
  );
};

export default BotDetails;
