// import axios from "axios";
// import Cookies from "js-cookie";
// import { TradingDataContext } from "@/common/hooks/TradingDataContext";
import useCookie from "@/common/hooks/useCookie";
// import React from "react";
import { Navigate, Outlet } from "react-router-dom";



const ProtectedRoute = () => {

    const [access_token] = useCookie("access_token", "");
    // If i fetch user profile here to auth, will fail, idk why...
    // const { auth } = React.useContext(TradingDataContext);
    // console.log("You are authenticated?", auth);

    // TODO 重新整理之後會一開始auth = false但點分頁會變成true 怪怪
  return access_token ? <Outlet /> : <Navigate to="/" />;
};

export default ProtectedRoute;
