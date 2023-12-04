import axios from "axios";
import React, { useEffect, useState, useContext } from "react";
import { useParams } from "react-router-dom";
import { TradingDataContext } from "@/common/hooks/TradingDataContext";
import { BotError, ContainerStateProps } from "../../models";
import { bot_api_base } from "@/common/apis";

const BotDetails: React.FC = () => {
  const { botId } = useParams<{ botId: string }>();
  const bot_api = bot_api_base(botId);
  const { botData, setBotData } = useContext(TradingDataContext);
  const [botErrors, setBotErrors] = useState<BotError[]>([]);
  const [containerData, setContainerData] = useState<
    ContainerStateProps[] | undefined
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
        setContainerData(response.data.data);
        console.log("set ContainerData:", response.data.data);
      } catch (error) {
        console.error("Error fetching container data:", error);
      }
    };

    fetchContainerData();
  }, [botId]);
  // Format the timestamp
  const formattedTimestamp = (timestamp: number) =>
    new Date(timestamp).toLocaleString();

  return (
    <div>
      {!botErrors || botErrors.length === 0 ? (
        <p>No trading error found</p>
      ) : (
        botErrors.map((error, index) => (
          <div key={index}>
            <p>{error.error}</p>
            <p>{new Date(error.timestamp).toLocaleString()}</p>
          </div>
        ))
      )}

      {!containerData || containerData.length === 0 ? (
        <p>No container info :(</p>
      ) : (
        containerData
          .filter((container) => container.bot_id == Number(botId))
          .map((data, i) => (
            <div key={i}>
              <p>container name: {data.container_name}</p>
              <p>
                運作狀態: {data.state} ({data.status})
              </p>
              <p>運作時間: {data.running_for}</p>
              <p>上次更新: {data.updated_at}</p>
              <ol>
                {data.logs.map((log, i) => (
                  <li key={i}>{log}</li>
                ))}
              </ol>
            </div>
          ))
      )}

      {botData && botData.length > 0 ? (
        <>
          <h1 className="text-xl font-bold mb-2">
            Bot Details: {botData[0].container_name}
          </h1>
          <div className="mb-4">
            <strong>Symbol:</strong> {botData[0].info.symbol}
          </div>
          {/* <div className="mb-4">
            <strong>Total Realized Pnl:</strong>{" "}
            {botData.reduce((sum, botDetail) => sum + botDetail.realizedPnl, 0)} (
            <span>
              {(
                ((botData.reduce(
                  (sum, botDetail) => sum + botDetail.realizedPnl,
                  0
                )) /
                  botData.reduce(
                    (sum, botDetail) =>
                      sum + botDetail.qty * botDetail.avg_price,
                    0
                  )) *
                100
              ).toFixed(2)}{" "}
              %)
            </span>
          </div> */}
          {botData.map((bot) => (
            <div
              key={bot.id}
              className="bg-gray-800 text-white p-4 rounded-lg shadow-lg m-2"
            >
              <div className="mb-4">
                <strong>Order id:</strong> {bot.order_id}
              </div>
              <div className="mb-4">
                <strong>Action:</strong> {bot.action}
              </div>
              <div className="mb-4">
                <strong>Average Price:</strong> {bot.avg_price.toFixed(2)}
              </div>
              <div className="mb-4">
                <strong>Quantity:</strong> {bot.qty}
              </div>
              <div className="mb-4">
                <strong>成交(USDT):</strong>{" "}
                {Number(bot.info.cumQuote).toFixed(2)}
              </div>
              <div className="mb-4">
                <strong>Realized Pnl:</strong> {bot.realizedPnl || 0}
              </div>
              <div className="mb-4">
                <strong>Side:</strong> {bot.info.side}
              </div>
              {/* <div className="mb-4">
                <strong>Type:</strong> {bot.info.type}
              </div> */}

              <div className="mb-4">
                <p>
                  <strong>Timestamp:</strong>{" "}
                  {formattedTimestamp(bot.timestamp)}
                </p>
              </div>
            </div>
          ))}
        </>
      ) : (
        <div>No bot data found</div>
      )}
    </div>
  );
};

export default BotDetails;
