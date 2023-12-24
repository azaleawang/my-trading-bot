import React, { createContext, useState, ReactNode, useEffect } from "react";
import { BotDetailsProps } from "../../pages/trading-bot/models";
import axios from "axios";
import useCookie from "./useCookie";


interface TradingDataContextProps {
  botData: BotDetailsProps[] | undefined;
  setBotData: (data: BotDetailsProps[] | undefined) => void; // Function to update botData
  auth: boolean;
  setAuth: (auth: boolean) => void;
  loading: boolean;
  setLoading: (loading: boolean) => void;
}
// interface Profile {
//   id: number;
//   name: string;
//   email: string;
// }

const defaultState: TradingDataContextProps = {
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
  const [botData, setBotData] = useState<BotDetailsProps[] | undefined>();
  const [auth, setAuth] = useState(false);
  const [loading, setLoading] = useState(true);
  const [access_token] = useCookie("access_token", "");

  const getProfile = async () => {
    try {
      await axios.get("/api/v1/users/profile", {
        headers: {
          Authorization: `Bearer ${access_token}`,
        },
      });
      setAuth(true);
    } catch (error: any) {
      setAuth(false);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    getProfile();
  }, []);

  return (
    <TradingDataContext.Provider
      value={{
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
