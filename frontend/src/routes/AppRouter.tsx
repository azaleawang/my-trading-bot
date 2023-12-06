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
import ProtectedRoute from "./ProtectedRoute";

const router = createBrowserRouter(
  createRoutesFromElements(
    <>
      <Route path="/" element={<Layout />}>
        <Route index element={<Home />} />
        <Route element={<ProtectedRoute />}>
          <Route path="/trading-bots" element={<BotContainer />} />
          <Route path="/trading-bots/:botId" element={<BotDetails />} />
          <Route path="/create-bot" element={<CreateBotForm />} />
        </Route>

        <Route path="/backtest" element={<Backtest />} />
      </Route>
      <Route path="*" element={<Navigate to="/" />} />
    </>
  )
);

export default router;
