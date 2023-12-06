import React from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import Cookies from "js-cookie";
import useCookie from "@/common/hooks/useCookie";
import { TradingDataContext } from "@/common/hooks/TradingDataContext";

const SignButton: React.FC = () => {
  const navigate = useNavigate();
  const { auth } = React.useContext(TradingDataContext);
  // const [user_id, updateCookie] = useCookie("user_id", "");
  // const [access_token, updateCookie] = useCookie("access_token", "");
  const handleSignout = (event: React.MouseEvent<HTMLButtonElement>) => {
    event.preventDefault();
    if (auth && confirm("Are you sure you want to sign out?")) {
      try {
        
        Cookies.remove("access_token");
        Cookies.remove("user_id");
        navigate("/");
      } catch (error) {
        console.error("Error signing out:", error);
      }
    }

    return;
  };

  return (
    <Button
      onClick={handleSignout}
    >Sign Out
    </Button>
  );
};

export default SignButton;
