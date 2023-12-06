import React, { createContext, useState, ReactNode, useEffect } from "react";
import { BotDetailsProps } from "../../pages/trading-bot/models";
import axios from "axios";
import useCookie from "./useCookie";
// import { Outlet, Navigate } from "react-router-dom";

interface TradingDataContextProps {
  markPrice: string[] | null;
  setMarkPrice: (price: string[] | null) => void;
  botData: BotDetailsProps[] | undefined;
  setBotData: (data: BotDetailsProps[] | undefined) => void; // Function to update botData
  auth: boolean;
  setAuth: (auth: boolean) => void;
  // profile: Profile | undefined;
}
// interface Profile {
//   id: number;
//   name: string;
//   email: string;
// }

const defaultState: TradingDataContextProps = {
  markPrice: null,
  setMarkPrice: () => {},
  botData: undefined,
  setBotData: () => {},
  auth: false,
  setAuth: () => {},
  // profile: undefined,
  // setProfile: () => {},
};

export const TradingDataContext =
  createContext<TradingDataContextProps>(defaultState);

export const TradingDataProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const [markPrice, setMarkPrice] = useState<string[] | null>(null); // TODO 這個應該暫時用不到了
  const [botData, setBotData] = useState<BotDetailsProps[] | undefined>();
  const [auth, setAuth] = useState(false);
  const [access_token] = useCookie("access_token", "");
  // const [profile, setProfile] = useState<Profile>();
  const getProfile = async () => {
    if (!access_token) {
      console.log("No jwt token");
      setAuth(false);
      return;
    }
    try {
      const resp = await axios.get("/api/v1/user/profile", {
        headers: {
          Authorization: `Bearer ${access_token}`,
        },
      });
      console.log("jwt token is valid", "User = ", resp.data);
      // setProfile(resp.data);
      setAuth(true);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    getProfile();
  }, []);

  return (
    <TradingDataContext.Provider
      value={{
        markPrice,
        setMarkPrice,
        botData,
        setBotData,
        auth,
        setAuth,
        // profile,
      }}
    >
      {children}
    </TradingDataContext.Provider>
  );
};
