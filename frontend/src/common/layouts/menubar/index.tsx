import React from "react";
import { Link } from "react-router-dom";
import { Bot, Home, CandlestickChart } from "lucide-react";
const MenuBar: React.FC = () => {
  return (
    <>
      <ul className="flex space-x-5 text-slate-200 z-50 gap-5 ml-3">
        <li className="flex items-center">
          <Link to="/">
            <div className="flex gap-2 items-center">
              <Home size={22} />
              <p className="tracking-wider hidden sm:block">首頁</p>
            </div>
          </Link>
        </li>
        <li className="flex items-center">
          <Link to="/trading-bots">
            <div className="flex gap-2 items-center">
              <Bot size={25} />
              <p className="tracking-wider hidden sm:block">機器人</p>
            </div>
          </Link>
        </li>
        <li className="flex items-center">
          <Link to="/backtest">
            <div className="flex gap-2 items-center">
              <CandlestickChart size={25} />
              <p className="tracking-wider hidden sm:block">策略回測</p>
            </div>
          </Link>
        </li>
      </ul>
    </>
  );
};

export default MenuBar;
