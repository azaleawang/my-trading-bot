import React from "react";
import { Link } from "react-router-dom";

const MenuBar: React.FC = () => {
  return (
    <>
      <nav className="p-4 text-white sticky top-0" style={{backgroundColor: "#191919"}}  >
        {/* */}
        <ul className="flex space-x-4 text-slate-200">
          <li>
            <Link to="/">Home</Link>
          </li>
          {/* Assuming a static userId for demonstration; replace with dynamic userId as needed */}
          <li>
            <Link to="/trading-bots">Trading Bots</Link>
          </li>
          <li>
            <Link to="/create-bot">Create Bot</Link>
          </li>
          <li>
            <Link to="/backtest">Backtest</Link>
          </li>
        </ul>
      </nav>
    </>
  );
};

export default MenuBar;
