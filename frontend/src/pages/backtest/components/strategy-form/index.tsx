import useCookie from "@/common/hooks/useCookie";
import { Button } from "@/components/ui/button";
import axios from "axios";
import "./style.css";
import { useEffect, useState } from "react";
// import { useParams } from "react-router-dom";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { toast } from "react-toastify";

const symbolList = [
  "BTC/USDT",
  "ETH/USDT",
  "BNB/USDT",
  // "XRP/USDT",
  // "ADA/USDT",
  // "SOL/USDT",
  // "DOT/USDT",
  "DOGE/USDT",
  // "MATIC/USDT",
];

interface StrategyFormProps {
  setLoading: (loading: boolean) => void;
  setBacktestId: (id: number | undefined) => void;
}

const StrategyForm: React.FC<StrategyFormProps> = ({ setLoading, setBacktestId }) => {
  const backtest_api_base = `/api/v1/backtests/`;
  const strategy_api_base = `/api/v1/strategies/`;
  const [userId] = useCookie("user_id", "");
  // strategy data
  interface Strategies {
    name: string;
    file_url: string | null;
    provider_id: number;
    is_public: boolean;
    id: number;
    params: { [key: string]: any };
  }
  const [strategies, setStrategies] = useState<Strategies[]>([]); // strategies fetched from database

  // strategy chosen to be tested
  interface Bt_Strategy {
    name: string;
    symbols: string[];
    t_frame: string;
    since: string;
    default_type: string;
    params: { [key: string]: any };
    user_id: number
  }

  const [bt_strategy, setBt_strategy] = useState<Bt_Strategy>({
    name: "",
    symbols: ["BTC/USDT"],
    t_frame: "1d",
    since: "2023-01-01",
    default_type: "future",
    params: {},
    user_id: Number(userId)
  });

  useEffect(() => {
    const fetchStrategies = async () => {
      try {
        const response = await axios.get(
          `${strategy_api_base}?user_id=${userId}`
        );
        setStrategies(response.data);
      } catch (error) {
        console.error("Error fetching strategies:", error);
      }
    };

    fetchStrategies();
  }, []); // Empty dependency array to run only once on mount

  const handleOptionChange = (value: string, name: string) => {
    console.log("Selected value: ", value);
    console.log("Field name: ", name);
    if (name === "name") {
      if (strategies) {
        const selectedStrategy = strategies.find((s) => s.name === value);
        setBt_strategy({
          ...bt_strategy,
          name: value,
          params: { ...selectedStrategy?.params },
        });
      }
    } else if (name === "symbols") {
      setBt_strategy({ ...bt_strategy, [name]: [value] });
    } else {
      setBt_strategy({ ...bt_strategy, [name]: value });
    }
  };

  const handleInputChange = (event: any) => {
    const { name, value } = event.target;
    if (name === "name") {
      if (strategies) {
        const selectedStrategy = strategies.find((s) => s.name === value);
        setBt_strategy({
          ...bt_strategy,
          name: value,
          params: { ...selectedStrategy?.params },
        });
      }
    } else if (name === "symbols") {
      setBt_strategy({ ...bt_strategy, [name]: [value] });
    } else {
      setBt_strategy({ ...bt_strategy, [name]: value });
    }
  };

  const handleParamChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    console.log(name, value);
    if (Number(value)) {
      setBt_strategy((prevStrategy) => ({
        ...prevStrategy,
        params: {
          ...prevStrategy.params,
          [name]: Number(value),
        },
      }));
    }
  };

  const handleSubmit = async (event: any) => {
    event.preventDefault();

    try {
      const isoDateString = new Date(bt_strategy.since).toISOString();

      const submissionData = {
        ...bt_strategy,
        since: isoDateString, // Use the ISO string format
      };
      console.log("submissionData", submissionData);
      const resp: any = await axios.post(backtest_api_base, submissionData);
      setLoading(true);
      setBacktestId(undefined);
      console.log(resp.data.message);
      toast.info("計算中，喝杯茶稍等 🍵");
    } catch (error: any) {
      console.error(error.response.data);
      setLoading(false);
      toast.error(
        error.response.data?.message ||
          "Something went wrong when submitting backtest"
      );
    }
  };

  return !strategies ? (
    <h1>No strategies found</h1>
  ) : (
    <div className="w-10/12 p-5 m-auto text-white">
      {/* <h1 className="mb-4">送出回測表單後，請耐心等待結果不要離開唷 ^^</h1> */}
      <form
        onSubmit={handleSubmit}
        className="flex  gap-5 mt-5 flex-wrap justify-between"
      >
        <div className="flex flex-wrap gap-5">
          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">策略名稱</label>
            <Select
              name="name"
              onValueChange={(value) => handleOptionChange(value, "name")}
              required
            >
              <SelectTrigger className="w-[180px] bg-inherit">
                <SelectValue placeholder="請選取策略" />
              </SelectTrigger>
              <SelectContent className="text-white bg-zinc-900">
                {strategies.map((s: Strategies, i) => (
                  <SelectItem key={i} value={s.name}>{s.name}</SelectItem>
                ))}
              </SelectContent>
            </Select>
            
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">交易對</label>
            <Select
              name="symbols"
              onValueChange={(value) => handleOptionChange(value, "symbols")}
              defaultValue="BTC/USDT"
            >
              <SelectTrigger className="w-[140px] bg-inherit text-white">
                <SelectValue placeholder="交易對" />
              </SelectTrigger>
              <SelectContent className="text-white bg-zinc-900">
                {symbolList.map((symbol, i) => (
                  <SelectItem key={i} value={symbol}>{symbol}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">時框</label>
            <Select
              name="t_frame"
              onValueChange={(value) => handleOptionChange(value, "t_frame")}
              defaultValue="1d"
            >
              <SelectTrigger className="w-[90px] bg-inherit">
                <SelectValue placeholder="時框" />
              </SelectTrigger>
              <SelectContent className="text-white bg-zinc-900">
                <SelectItem value="1d">1 day</SelectItem>
                <SelectItem value="4h">4 hour</SelectItem>
              </SelectContent>
            </Select>
            
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">起始時間</label>
            <input
              type="date"
              name="since"
              value={bt_strategy.since}
              onChange={handleInputChange}
              className="text-white flex h-10 w-full items-center justify-between rounded-md border border-input bg-inherit px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 [&>span]:line-clamp-1"
              required
            />
          </div>
        </div>
        <div className="flex">
          <div className="flex gap-5 flex-wrap mb-3">
            {strategies
              .filter((s: any) => s.name === bt_strategy.name)
              .map((selectedStrategy: Strategies) =>
                Object.entries(selectedStrategy.params).map(
                  ([paramKey, paramValue]) => (
                    <div key={paramKey}>
                      <label className="block text-sm font-medium mb-2">
                        {paramKey}
                      </label>
                      <input
                        type="number"
                        min="1"
                        name={paramKey}
                        value={bt_strategy.params[paramKey] || paramValue}
                        onChange={handleParamChange}
                        className="p-2 bg-inherit border-b-2 focus:outline-none w-[70px]"
                        required
                      />
                    </div>
                  )
                )
              )}
          </div>
        </div>
        <div className="flex items-center justify-center">
          <Button
            type="submit"
            className="px-6 py-2 rounded bg-zinc-700 hover:bg-zinc-600"
          >
            <p className="tracking-widest	font-medium">開始回測</p>
          </Button>
        </div>
      </form>
    </div>
  );
};

export default StrategyForm;
