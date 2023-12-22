import axios from "axios";
import useCookie from "@/common/hooks/useCookie";
// import React from "react";
import { useContext, useEffect, useState } from "react";
import { useNavigate, Outlet, useLocation } from "react-router-dom";
import { toast } from "react-toastify";
import { TradingDataContext } from "@/common/hooks/TradingDataContext";
// interface Profile {
//   id: number;
//   name: string;
//   email: string;
// }
export default function ProtectedRoute() {
  const [error, setError] = useState<unknown>();
  // const [loading, setLoading] = useState(true);
  const { loading } = useContext(TradingDataContext);
  const { auth } = useContext(TradingDataContext);

  // const [access_token] = useCookie("access_token", "");
  const navigate = useNavigate();
  const location = useLocation();
  // 直接抓auth state看有沒有權限 不用再抓profile 還有loading state也要移到context

  useEffect(() => {
    const checkAuthentication = async () => {
      try {
        if (!auth) navigate("/login");
        console.log("auth is ", auth);
      } catch (error: any) {
        console.log("error", error);
        if (error?.response.status === 403) {
          toast.warn("唉呀！忘了登入啦！", {});
          navigate("/login");
        } else setError(error);
      }
    };

    checkAuthentication();
  }, [navigate, location]);

  if (error) {
    navigate("/");
  }

  return loading ? <></> : <Outlet />;
}
