import axios from "axios";
import useCookie from "@/common/hooks/useCookie";
// import React from "react";
import { useEffect, useState } from "react";
import { useNavigate, Outlet, useLocation } from "react-router-dom";
interface Profile {
  id: number;
  name: string;
  email: string;
}
export default function ProtectedRoute() {
  const [error, setError] = useState<unknown>();
  const [loading, setLoading] = useState(true);
  const [access_token] = useCookie("access_token", "");
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const checkAuthentication = async () => {
      try {
        const resp = await axios.get("/api/v1/user/profile", {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        });

        const profile: Profile = resp.data;

        if (!profile) {
          console.log("You are not authenticated!");
          navigate("/");
        } else {
          // setIsAuth(true);
          setLoading(false);
          console.log("You are authenticated!");
        }
      } catch (error) {
        console.log("error", error);
        setError(error);
      }
    };

    checkAuthentication();
  }, [navigate, location]);

  if (error) {
    navigate("/");
  }

  return loading ? <></>: <Outlet />;
}

