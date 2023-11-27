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
import BotDetails from "../pages/trading-bot/components/bot-details";
import Layout from "../common/layouts";

const router = createBrowserRouter(
  createRoutesFromElements(
    <>
      <Route path="/" element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="/user/:userId/trading-bots" element={<BotContainer />} />
        <Route
          path="/user/:userId/trading-bots/:botId"
          element={<BotDetails />}
        />
        <Route path="/user/:userId/create-bot" element={<CreateBotForm />} />
        <Route path="/backtest" element={<Backtest />} />
      {/* <Route path="/run-backtest" element={<StrategyForm />} /> */}
      </Route>
      <Route path="*" element={<Navigate to="/" />} />
    </>
  )
);

export default router;
