import React from "react";
import { Link } from "react-router-dom";

const MenuBar: React.FC = () => {
  return (
    <>
      <ul className="flex space-x-5 text-slate-200 z-50">
        <li className="flex items-center">
          <Link to="/">首頁</Link>
        </li>
        <li className="flex items-center">
          <Link to="/trading-bots">我的機器人</Link>
        </li>
        <li className="flex items-center">
          <Link to="/create-bot">新增機器人</Link>
        </li>
        <li className="flex items-center">
          <Link to="/backtest">策略回測</Link>
        </li>
      </ul>
    </>
  );
};

export default MenuBar;
