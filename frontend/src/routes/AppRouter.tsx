import {
  createBrowserRouter,
  Route,
  createRoutesFromElements,
  Navigate,
} from "react-router-dom";
import BotContainer from "../pages/trading-bot/components/bot-container";
import Home from "../pages/home";
import CreateBotForm from "../pages/create-bot/components/form";
import Backtest from "../pages/backtest/components/complete-result";
import StrategyForm from "../pages/run-backtest/components/strategy-form";

const router = createBrowserRouter(
  createRoutesFromElements(
    <>
      <Route path="/" element={<Home />} />
      <Route path="/trading-bots" element={<BotContainer />} />
      {/* <Route path="/trading-bots/:botId" element={<BotContainer />} /> */}
      <Route path="/create-bot" element={<CreateBotForm />} />
      <Route path="/backtest" element={<Backtest />} />
      <Route path="/run-backtest" element={<StrategyForm />} />

      <Route path="*" element={<Navigate to="/" />} />
    </>
  )
);

export default router;