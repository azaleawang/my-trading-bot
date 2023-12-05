import useCookie from "@/common/hooks/useCookie";
import axios from "axios";
import { useEffect, useState } from "react";
// import { useParams } from "react-router-dom";

const StrategyForm = () => {
  const backtest_api_base = `/api/v1/backtests/`;
  const strategy_api_base = `/api/v1/strategies/`;
  const [userId] = useCookie("user_id", "");

  // strategy data
  interface AllStrategies {
    name: string;
    file_url: string | null;
    provider_id: number;
    is_public: boolean;
    id: number;
    params: { [key: string]: any };
  }
  const [strategies, setStrategies] = useState<AllStrategies[]>([]); // strategies fetched from database

  // strategy chosen to be tested
  interface Bt_Strategy {
    name: string;
    symbols: string[];
    t_frame: string;
    since: string;
    default_type: string;
    params: { [key: string]: any };
  }

  const [bt_strategy, setBt_strategy] = useState<Bt_Strategy>({
    name: "",
    symbols: ["BTC/USDT"],
    t_frame: "1d",
    since: "2023-01-01",
    default_type: "future",
    params: {},
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
    console.log("Submitting Strategy", bt_strategy);

    try {
      const isoDateString = new Date(bt_strategy.since).toISOString();

      const submissionData = {
        ...bt_strategy,
        since: isoDateString, // Use the ISO string format
      };
      const resp: any = await axios.post(backtest_api_base, submissionData);
      console.log(resp.data.message);
      alert("Start running backtest");
    } catch (error: any) {
      console.error(error.response.data);
      alert(
        error.response.data?.message ||
          "Something went wrong when submitting backtest"
      );
    }
  };

  return !strategies ? (
    <h1>No strategies found</h1>
  ) : (
    <div className="max-w-lg mx-auto my-10 p-6 bg-gray-800 text-white rounded-lg shadow-xl">
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-sm font-medium mb-2">Strategy:</label>
          <select
            name="name"
            value={bt_strategy.name}
            onChange={handleInputChange}
            className="w-full p-2 rounded bg-gray-700 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          >
            <option value="">Select a strategy</option>
            {strategies.map((s: any, i) => (
              <option value={s.name} key={i}>
                {s.name}
              </option>
            ))}
            {/* <option value="MaRsi">MaRsi</option>
            <option value="MaCrossover">MaCrossover</option>
            <option value="SuperTrend">SuperTrend</option>
            <option value="RsiOscillator">RsiOscillator</option> */}
          </select>
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium mb-2">Symbols:</label>
          <select
            name="symbols"
            value={bt_strategy.symbols}
            onChange={handleInputChange}
            className="w-full p-2 rounded bg-gray-700 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          >
            <option value="">Select a symbol</option>
            <option value="BTC/USDT">BTC/USDT</option>
            <option value="ETH/USDT">ETH/USDT</option>
            <option value="XRP/USDT">XRP/USDT</option>
          </select>
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium mb-2">Time Frame:</label>
          <select
            name="t_frame"
            value={bt_strategy.t_frame}
            onChange={handleInputChange}
            className="w-full p-2 rounded bg-gray-700 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          >
            <option value="1d">1 day</option>
            <option value="4h">4 hours</option>
            <option value="1h">1 hour</option>
          </select>
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium mb-2">Since:</label>
          <input
            type="date"
            name="since"
            value={bt_strategy.since}
            onChange={handleInputChange}
            className="w-full p-2 rounded bg-gray-700 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        {strategies
          .filter((s: any) => s.name === bt_strategy.name)
          .map((selectedStrategy: any) =>
            Object.entries(selectedStrategy.params).map(
              ([paramKey, paramValue]) => (
                <div className="mb-6" key={paramKey}>
                  <label className="block text-sm font-medium mb-2">
                    {paramKey}
                  </label>
                  <input
                    type="number"
                    min="1"
                    name={paramKey}
                    value={bt_strategy.params[paramKey] || paramValue}
                    onChange={handleParamChange}
                    className="w-full p-2 rounded bg-gray-700 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
              )
            )
          )}

        <div className="flex justify-end">
          <button
            type="submit"
            className="px-6 py-2 rounded bg-blue-500 hover:bg-blue-700 transition-colors duration-300 ease-in-out"
          >
            Go
          </button>
        </div>
      </form>
    </div>
  );
};

export default StrategyForm;
