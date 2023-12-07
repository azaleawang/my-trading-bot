import React, { useState } from "react";
import Cookies from "js-cookie";

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

interface UserAuthFormProps extends React.HTMLAttributes<HTMLDivElement> {}

export function UserAuthForm({ className, ...props }: UserAuthFormProps) {
  const [isLoading, setIsLoading] = React.useState<boolean>(false);
  const [email, setEmail] = useState<string>("test@test.com");
  const [password, setPassword] = useState<string>("string");
  const [name, setName] = useState<string>("test");
  // const [setAccessToken] = useCookie("access_token", "");
  // const [setUserId] = useCookie("user_id", "");
  const navigate = useNavigate();
  const { setAuth } = React.useContext(TradingDataContext);

  // TODO: add validation for name, email and password
  function validateInput(name: string, email: string, password: string) {
    if (!name.trim() || !email.trim() || !password.trim()) {
      throw new Error("請填入所有欄位");
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
      setAuth(true);
      alert("註冊成功，請登入後使用"); // TODO should be a dialog or toast
    } catch (error: any) {
      console.error("Sign in failed", error);
      alert(
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
      setAuth(true);
      alert("Login successful"); // TODO should be a dialog or toast
      // navigate to trading bots page
      navigate(`/trading-bots`);
    } catch (error: any) {
      console.error("Sign in failed", error);
      alert(
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
              {/* <CardDescription>
                Make changes to your account here. Click save when you're done.
              </CardDescription> */}
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
              {/* <CardDescription>
                Change your password here. After saving, you'll be logged out.
              </CardDescription> */}
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

      {/* <div className={cn("grid gap-6", className)} {...props}>
        <form handleLogin={handleLogin}>
          <div className="grid gap-2">
            <div className="grid gap-1">
              <Label className="sr-only" htmlFor="email">
                Email
              </Label>
              <Input
                id="email"
                placeholder="name@example.com"
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
            <div className="grid gap-1">
              <Label className="sr-only" htmlFor="password">
                Password
              </Label>
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
            <Button disabled={isLoading}>
              {isLoading && (
                <Icons.spinner className="mr-2 h-4 w-4 animate-spin" />
              )}
              Sign In with Email
            </Button>
          </div>
        </form>
        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <span className="w-full border-t" />
          </div>
          <div className="relative flex justify-center text-xs uppercase">
            <span className="bg-black text-white px-2 text-muted-foreground">
              Or continue with
            </span>
          </div>
        </div>
        <Button variant="outline" type="button" disabled={isLoading}>
          {isLoading ? (
            <Icons.spinner className="mr-2 h-4 w-4 animate-spin" />
          ) : (
            <Icons.gitHub className="mr-2 h-4 w-4" />
          )}{" "}
          Github
        </Button>
      </div> */}
    </>
  );
}
