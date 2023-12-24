import { useContext, useEffect } from "react";
import { useNavigate, Outlet, useLocation } from "react-router-dom";
import { TradingDataContext } from "@/common/hooks/TradingDataContext";
import { toast } from "react-toastify";

export default function ProtectedRoute() {
  const { loading, auth } = useContext(TradingDataContext);

  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const checkAuthentication = async () => {
      if (!auth && !loading) {
        // TODO why must add !loading?
        toast.error("您忘記登入啦~", {
          autoClose: 1000,
        });
        navigate("/login");
      }
    };

    checkAuthentication();
  }, [navigate, location]);

  return loading ? <></> : <Outlet />;
}
