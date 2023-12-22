import React, { createContext, useState, ReactNode, useEffect } from "react";
import { BotDetailsProps } from "../../pages/trading-bot/models";
import axios from "axios";
import useCookie from "./useCookie";
import { useNavigate } from "react-router-dom";
// import { Outlet, Navigate } from "react-router-dom";

interface TradingDataContextProps {
  markPrice: string[] | null;
  setMarkPrice: (price: string[] | null) => void;
  botData: BotDetailsProps[] | undefined;
  setBotData: (data: BotDetailsProps[] | undefined) => void; // Function to update botData
  auth: boolean;
  setAuth: (auth: boolean) => void;
  loading: boolean;
  setLoading: (loading: boolean) => void;
}
interface Profile {
  id: number;
  name: string;
  email: string;
}

const defaultState: TradingDataContextProps = {
  markPrice: null,
  setMarkPrice: () => {},
  botData: undefined,
  setBotData: () => {},
  auth: false,
  setAuth: () => {},
  loading: false,
  setLoading: () => {},
};

export const TradingDataContext =
  createContext<TradingDataContextProps>(defaultState);

export const TradingDataProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  // const [error, setError] = useState<unknown>();
  const [markPrice, setMarkPrice] = useState<string[] | null>(null); // TODO 這個應該暫時用不到了
  const [botData, setBotData] = useState<BotDetailsProps[] | undefined>();
  const [auth, setAuth] = useState(false);
  const [loading, setLoading] = useState(true);
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

      const profile: Profile = resp.data;

      if (!profile) {
        console.log("You are not authenticated!");
      } else {
        setAuth(true);
        setLoading(false);
        console.log("You are authenticated!");
      }
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
        loading,
        setLoading,
      }}
    >
      {children}
    </TradingDataContext.Provider>
  );
};
