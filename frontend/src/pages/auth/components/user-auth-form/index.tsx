import React, { useState } from "react";
import Cookies from "js-cookie";
import { toast } from "react-toastify";

import "react-toastify/dist/ReactToastify.css";
import { Icons } from "@/components/ui/icons";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { TradingDataContext } from "@/common/hooks/TradingDataContext";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export function UserAuthForm() {
  const [isLoading, setIsLoading] = React.useState<boolean>(false);
  const [email, setEmail] = useState<string>("test@test.com");
  const [password, setPassword] = useState<string>("string");
  const [name, setName] = useState<string>("test");
  const navigate = useNavigate();
  const { setAuth } = React.useContext(TradingDataContext);
  function validateInput(name: string, email: string, password: string) {
    if (!name.trim() || !email.trim() || !password.trim()) {
      throw new Error("請填入所有欄位");
    }
    const chineseRegex = /[\u4E00-\u9FFF]/;

    if (chineseRegex.test(email) || chineseRegex.test(password)) {
      throw new Error("不接受中文輸入");
    }
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      throw new Error("Email is not valid");
    }
    if (name.trim().length < 2 || name.trim().length > 20) {
      throw new Error("Username must be between 2 to 20 characters");
    }
    if (password.trim().length <= 3) {
      throw new Error("Password must be longer than 3 characters");
    }
  }

  async function handleSignup(event: React.SyntheticEvent) {
    event.preventDefault();
    setIsLoading(true);

    try {
      const signupData = {
        name: name,
        email: email,
        password,
      };

      validateInput(signupData.name, signupData.email, signupData.password);
      const response = await axios.post(
        `${import.meta.env.VITE_HOST}/signup`,
        signupData
      );
      console.log(response.data);

      toast.success("註冊成功，請登入後使用", {
        autoClose: 1000,
      });
    } catch (error: any) {
      console.error("Sign in failed", error);
      toast.error(
        error.response?.data?.detail ||
          error.message ||
          "Something went wrong when signin"
      );
    } finally {
      setIsLoading(false);
    }
  }

  async function handleLogin(event: React.SyntheticEvent) {
    event.preventDefault();
    setIsLoading(true);

    try {
      const loginData = {
        email: email,
        password: password,
      };

      validateInput("placeholder", loginData.email, loginData.password);
      const response = await axios.post(
        `${import.meta.env.VITE_HOST}/login`,
        loginData
      );
      console.log(response.data);
      Cookies.set("access_token", response.data.access_token, { expires: 1 });
      Cookies.set("user_id", response.data.user_id, { expires: 1 });
      Cookies.set("username", response.data.username, { expires: 1 });
      setAuth(true);
      toast.success("登入成功！", {
        autoClose: 1000,
      });
      navigate(-1);
    } catch (error: any) {
      console.error("Sign in failed", error);
      toast.error(
        error.response?.data?.detail ||
          error.message ||
          "Something went wrong when signin"
      );
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <>
      <Tabs defaultValue="account" className="w-[350px]">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="account">登入</TabsTrigger>
          <TabsTrigger value="password">註冊</TabsTrigger>
        </TabsList>
        <TabsContent value="account">
          <Card>
            <CardHeader>
              <CardTitle>嗨！歡迎回來！</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <div className="space-y-1">
                <Label htmlFor="email">信箱</Label>
                <Input
                  id="email"
                  placeholder="test@test.com"
                  type="email"
                  autoCapitalize="none"
                  autoComplete="email"
                  autoCorrect="off"
                  disabled={isLoading}
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
              <div className="space-y-1">
                <Label htmlFor="password">密碼</Label>
                <Input
                  id="password"
                  placeholder="password"
                  type="password"
                  autoCapitalize="none"
                  autoCorrect="off"
                  disabled={isLoading}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>
            </CardContent>
            <CardFooter>
              <Button
                disabled={isLoading}
                className="w-full mt-2"
                onClick={handleLogin}
              >
                {isLoading && (
                  <Icons.spinner className="mr-2 h-4 w-4 animate-spin" />
                )}
                確認登入
              </Button>
            </CardFooter>
          </Card>
        </TabsContent>
        <TabsContent value="password">
          <Card>
            <CardHeader>
              <CardTitle>歡迎新朋朋加入！</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <div className="space-y-1">
                <Label htmlFor="name">用戶暱稱</Label>
                <Input
                  id="username"
                  placeholder="test"
                  type="text"
                  autoCapitalize="none"
                  autoCorrect="off"
                  disabled={isLoading}
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                />
              </div>
              <div className="space-y-1">
                <Label htmlFor="email">信箱</Label>
                <Input
                  id="email"
                  placeholder="test@test.com"
                  type="email"
                  autoCapitalize="none"
                  autoComplete="email"
                  autoCorrect="off"
                  disabled={isLoading}
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
              <div className="space-y-1">
                <Label htmlFor="password">密碼</Label>
                <Input
                  id="password"
                  placeholder="password"
                  type="password"
                  autoCapitalize="none"
                  autoCorrect="off"
                  disabled={isLoading}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>
            </CardContent>
            <CardFooter>
              <Button
                disabled={isLoading}
                className="w-full mt-2"
                onClick={handleSignup}
              >
                {isLoading && (
                  <Icons.spinner className="mr-2 h-4 w-4 animate-spin" />
                )}
                我要註冊
              </Button>
            </CardFooter>
          </Card>
        </TabsContent>
      </Tabs>
    </>
  );
}
