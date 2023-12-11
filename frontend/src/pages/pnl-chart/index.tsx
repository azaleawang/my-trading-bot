import { bot_api_base } from "@/common/apis";
import axios from "axios";
import { useEffect, useState } from "react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";

interface PnlData {
  pnl: number;
  timestamp: number;
}

const MyAreaChart = () => {
  const [pnlData, setPnlData] = useState<PnlData[]>([]); // const userId = 1;
  const botId = 20;
  // const rawData = [
  //   { pnl: -4.83644, timestamp: 1702080000000 },
  //   { pnl: -6.04348, timestamp: 1702111500000 },
  //   { pnl: -1.03546, timestamp: 1702138500000 },
  //   { pnl: 4.03546, timestamp: 1703138500000 },
  //   { pnl: 0.03546, timestamp: 1704138500000 },
  // ];

  // fetch data from server to draw chart
  useEffect(() => {
    // fetch data from server
    const fetchPnlData = async () => {
      try {
        const response = await axios.get(`${bot_api_base(botId)}/pnl-chart`);
        console.log("response", bot_api_base(botId))
        const data = response.data.data;
        console.log("data", data)
        setPnlData(data);
        
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchPnlData();
  }, [botId]);

  if (!pnlData || pnlData.length === 0) {
    return <div>Loading...</div>;
  }

  // 將 timestamp 轉換為可讀的日期或時間格式
  const data = pnlData.map((item) => {
    const date = new Date(item.timestamp);
    const formattedDate = `${
      date.getMonth() + 1
    }-${date.getDate()} ${date.getHours()}:${date.getMinutes()}`;
    return { ...item, timestamp: formattedDate };
  });
  return (
    <AreaChart
      width={730}
      height={250}
      data={data}
      margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
    >
      <defs>
        <linearGradient id="colorPnl" x1="0" y1="0" x2="0" y2="1">
          <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8} />
          <stop offset="95%" stopColor="#8884d8" stopOpacity={0} />
        </linearGradient>
      </defs>
      <XAxis dataKey="timestamp" />
      <YAxis />
      <CartesianGrid strokeDasharray="3 3" />
      <Tooltip />
      <Area
        type="monotone"
        dataKey="pnl"
        stroke="#8884d8"
        fillOpacity={1}
        fill="url(#colorPnl)"
      />
    </AreaChart>
  );
};

export default MyAreaChart;
