import React from "react";

// Update these imports according to your project structure
import { UserAuthForm } from "../user-auth-form";
import { TradingDataContext } from "@/common/hooks/TradingDataContext";
import { Navigate } from "react-router-dom";

const AuthenticationPage: React.FC = () => {
  const { auth } = React.useContext(TradingDataContext);
  return (
    <div className="container my-auto relative h-[400px] flex-col items-center justify-center flex">
      {!auth ? <UserAuthForm /> : <Navigate to="/trading-bots" />}
    </div>
  );
};

export default AuthenticationPage;
