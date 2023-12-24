import React, { useContext } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import Cookies from "js-cookie";
import { TradingDataContext } from "@/common/hooks/TradingDataContext";

const SignButton: React.FC = () => {
  const navigate = useNavigate();
  const { auth } = useContext(TradingDataContext);
  // const [user_id, updateCookie] = useCookie("user_id", "");
  // const [access_token, updateCookie] = useCookie("access_token", "");
  const handleSignout = (event: React.MouseEvent<HTMLButtonElement>) => {
    event.preventDefault();
    if (auth && confirm("確定要登出嗎 🤔")) {
      try {
        Cookies.remove("access_token");
        Cookies.remove("user_id");
        Cookies.remove("username");
        window.location.replace("/");
      } catch (error) {
        console.error("Error signing out:", error);
      }
    }

    return;
  };

  if (!auth) {
    return (
      <Button
        onClick={() => {
          navigate("/login");
        }}
      >
        Sign In
      </Button>
    );
  }
  return <Button onClick={handleSignout}>Sign Out</Button>;
};

export default SignButton;
