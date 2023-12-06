import React from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import Cookies from "js-cookie";

const SignoutButton: React.FC = () => {
  const navigate = useNavigate();
  const handleSignout = (event: React.MouseEvent<HTMLButtonElement>) => {
    event.preventDefault();
    if (confirm("Are you sure you want to sign out?")) {
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
    //   style={{ backgroundColor: "lightgrey", color: "dark" }}
    >
      Sign Out
    </Button>
  );
};

export default SignoutButton;
