import { useContext } from "react";

// Update these imports according to your project structure
import { UserAuthForm } from "../user-auth-form";
import { TradingDataContext } from "@/common/hooks/TradingDataContext";

const AuthenticationPage: React.FC = () => {
  const { auth } = useContext(TradingDataContext);
  return (
    <div className="container my-auto relative h-[400px] flex-col items-center justify-center flex">
      {!auth ? <UserAuthForm /> : <></>}
    </div>
  );
};

export default AuthenticationPage;
