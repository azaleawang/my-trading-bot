import React from "react";
import { Link } from "react-router-dom";

const MenuBar: React.FC = () => {
  return (
    <>
      <nav className="bg-gray-800 p-4 text-white">
        <ul className="flex space-x-4">
          <li>
            <Link to="/">Home</Link>
          </li>
          {/* Assuming a static userId for demonstration; replace with dynamic userId as needed */}
          <li>
            <Link to="/user/1/trading-bots">Trading Bots</Link>
          </li>
          <li>
            <Link to="/user/1/create-bot">Create Bot</Link>
          </li>
          <li>
            <Link to="/user/1/backtest">Backtest</Link>
          </li>
        </ul>
      </nav>
    </>
  );
};

export default MenuBar;
