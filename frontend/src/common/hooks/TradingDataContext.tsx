import React, { createContext, useState, ReactNode, useEffect } from "react";
import {
  BotDetailsProps,
  ContainerStateProps,
} from "../../pages/trading-bot/models";

interface TradingDataContextProps {
  markPrice: string[] | null;
  setMarkPrice: (price: string[] | null) => void;
  botData: BotDetailsProps[] | undefined;
  setBotData: (data: BotDetailsProps[] | undefined) => void; // Function to update botData
  containerData: ContainerStateProps[] | undefined;
  setContainerData: (data: ContainerStateProps[] | undefined) => void;
}

const defaultState: TradingDataContextProps = {
  markPrice: null,
  setMarkPrice: () => {},
  botData: undefined,
  setBotData: () => {},
  containerData: undefined,
  setContainerData: () => {},
};

export const TradingDataContext =
  createContext<TradingDataContextProps>(defaultState);

export const TradingDataProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const [markPrice, setMarkPrice] = useState<string[] | null>(null); // TODO 這個應該暫時用不到了
  const [botData, setBotData] = useState<BotDetailsProps[] | undefined>();
  const [containerData, setContainerData] = useState<
    ContainerStateProps[] | undefined
  >();

  // You can also add logic to fetch data here

  return (
    <TradingDataContext.Provider
      value={{
        containerData,
        setContainerData,
        markPrice,
        setMarkPrice,
        botData,
        setBotData,
      }}
    >
      {children}
    </TradingDataContext.Provider>
  );
};
