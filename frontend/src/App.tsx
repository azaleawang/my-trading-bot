import { RouterProvider } from 'react-router-dom';
import AppRouter from './routes/AppRouter';
import { TradingDataProvider } from "./common/hooks/TradingDataContext";
function App() {
  return (
    <TradingDataProvider>    
      <RouterProvider router={AppRouter} />
    </TradingDataProvider>
  );
}

export default App;
