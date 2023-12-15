import { bot_api_base } from "@/common/apis";
import useCookie from "@/common/hooks/useCookie";
import { Icons } from "@/components/ui/icons";
import axios from "axios";
import { useEffect, useState } from "react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

interface PnlData {
  pnl: number;
  timestamp: number;
}

interface PnlChartProps {
  botId: number | string;
}

const PnlChart = ({ botId }: PnlChartProps) => {
  const [pnlData, setPnlData] = useState<PnlData[]>([{
    pnl: 1,
    timestamp: 1702396800
  }, {
    pnl: 2,
    timestamp: 1702396810
  }, {
    pnl: 3,
    timestamp: 1702396900
  }]); // const userId = 1;
  const [loading, setLoading] = useState<boolean>(true);
  const [access_token] = useCookie("access_token", "");

  // fetch data from server to draw chart
  useEffect(() => {
    // fetch data from server
    const fetchPnlData = async () => {
      try {
        const response = await axios.get(`${bot_api_base(botId)}/pnl-chart`,
        {
          headers: {
            "Authorization": `Bearer ${access_token}`,
          },
        });
        console.log("response", bot_api_base(botId));
        const data = response.data.data;
        console.log("data", data);
        setPnlData(data);
        setLoading(false);
      } catch (error) {
        setLoading(false);
        console.error("Error fetching data:", error);
      }
    };

    fetchPnlData();
  }, [botId]);


  if (loading) {
    return (
      <div className="text-xl text-slate-400 flex justify-center h-[300px]">
        <Icons.spinner className="mr-5 h-[30px] w-[30px] animate-spin" />
        <span>Loading...</span>
      </div>
    );
  }
  if (!pnlData || pnlData.length === 0) {
    return <h1 className="text-xl text-slate-400 flex p-5">暫無圖表資訊</h1>;
  }

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const date = new Date(label as number); // 假設 label 是 timestamp
      const formattedDate = `${date.getMonth() + 1}/${date.getDate()} ${date
        .getHours()
        .toString()
        .padStart(2, "0")}:${date
        .getMinutes()
        .toString()
        .padStart(2, "0")}:${date.getSeconds().toString().padStart(2, "0")}`;

      return (
        <div
          className={`bg-white bg-opacity-70 p-3 border border-gray-200 rounded shadow-lg text-sm text-gray-800`}
        >
          <p>{formattedDate}</p>
          <p>{`盈虧: ${payload[0].value.toFixed(4)}`}</p>
        </div>
      );
    }

    return null;
  };

  return (
    <div className="flex pr-5 justify-center h-[300px]">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart
          data={pnlData}
          margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
        >
          <defs>
            <linearGradient id="colorPnl" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#51A8DD" stopOpacity={0.8} />
              <stop offset="95%" stopColor="#51A8DD" stopOpacity={0} />
            </linearGradient>
          </defs>
          <XAxis
            dataKey="timestamp"
            type="number"
            domain={["dataMin", "dataMax"]}
            scale="time"
            // tickFormatter={(unixTime) => new Date(unixTime).toLocaleTimeString()}
            tickFormatter={(unixTime) => {
              const date = new Date(unixTime);
              // const month = date.getMonth() + 1; // 月份是從 0 開始的
              // const day = date.getDate();
              const hours = date.getHours();
              const minutes = date.getMinutes();
              const seconds = date.getSeconds();

              return `
            ${hours.toString().padStart(2, "0")}:${minutes
                .toString()
                .padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
            }}
          />
          <YAxis />
          {/* <CartesianGrid strokeDasharray="3 3" /> */}
          {/* <Tooltip /> */}
          <Tooltip content={<CustomTooltip />} />

          <Area
            type="monotone"
            dataKey="pnl"
            // stroke="#58B2DC"
            fillOpacity={1}
            fill="url(#colorPnl)"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PnlChart;
