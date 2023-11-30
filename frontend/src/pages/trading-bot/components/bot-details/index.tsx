import axios from "axios";
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

interface BotDetailsProps {
  id: number;
  container_name: string;
  action: string;
  order_id: number;
  qty: number;
  avg_price: number;
  realizedPnl: number;
  info: {
    side: string;
    type: string;
    symbol: string;
    // ... other properties ...
  };
  timestamp: number;
}

const BotDetails: React.FC = () => {
  const { userId, botId } = useParams<{ userId: string; botId: string }>();
  //   TODO 把user id 補上
  const api_url = `/api/v1/bots/users/${userId}/bots/${botId}/trade-history`;

  const [botData, setBotData] = useState<BotDetailsProps[]>();

  useEffect(() => {
    const fetchBotDetails = async () => {
      try {
        // Replace with your actual API endpoint
        const response = await axios.get(api_url);
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

  // Render bot details or loading state
  if (!botData) {
    return <div>Loading bot details...</div>;
  }

  // Format the timestamp
  const formattedTimestamp = (timestamp: number) =>
    new Date(timestamp).toLocaleString();

  return (
    <div>
      {botData && botData.length > 0 ? (
        <>
          <h1 className="text-xl font-bold mb-2">
            Bot Details: {botData[0].container_name}
          </h1>
          <div className="mb-4">
            <strong>Symbol:</strong> {botData[0].info.symbol}
          </div>
          <div className="mb-4">
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
          </div>
          {botData.map((bot) => (
            <div
              key={bot.id}
              className="bg-gray-800 text-white p-4 rounded-lg shadow-lg m-2"
            >
              <div className="mb-4">
                <strong>Action:</strong> {bot.action}
              </div>
              <div className="mb-4">
                <strong>Average Price:</strong> {bot.avg_price}
              </div>
              <div className="mb-4">
                <strong>Order id:</strong> {bot.order_id}
              </div>
              <div className="mb-4">
                <strong>Quantity:</strong> {bot.qty}
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
