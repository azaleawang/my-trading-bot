import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { bot_api_base } from "@/common/apis";
import useCookie from "@/common/hooks/useCookie";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { toast } from "react-toastify";

const CreateBotForm: React.FC = () => {
  const navigate = useNavigate();
  const [userId] = useCookie("user_id", "");
  const [botData, setBotData] = useState({
    name: "Cool-bot",
    strategy: "supertrend",
    symbol: "ETH/USDT",
    description: "",
    t_frame: "30m",
    quantity: 120,
  });
  const strategies = ["supertrend"]; // only accept this strategy for now
  const symbols = ["ETH/USDT", "BNB/USDT", "BTC/USDT"]; // still hard-coded

  const handleOptionChange = (value: string, name: string) => {
    console.log("Selected value: ", value);
    console.log("Field name: ", name);
    setBotData({ ...botData, [name]: value });
  };

  const handleInputChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
    >
  ) => {
    setBotData({ ...botData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const nameRegex = /^[A-Za-z-_1234567890]+$/; // Only accept -,_ and alphabets
    if (!nameRegex.test(botData.name)) {
      toast.warn("名稱欄位僅接受英數 🙌");
      return;
    }

    const submissionData = {
      ...botData,
      owner_id: Number(userId),
      created_at: new Date().toISOString(),
    };
    try {
      console.log(submissionData);
      const response = await axios.post(
        `${bot_api_base(undefined)}/`,
        submissionData
      );
      console.log(response.data);
      if (
        confirm(
          `Bot ${response.data.data.name} created successfully! 交易對: ${response.data.data.symbol}`
        )
      ) {
        navigate(0);
      }

      // Handle the success (e.g., showing a notification, clearing the form, etc.)
    } catch (error: any) {
      console.error("Error creating bot:", error);
      toast.error(
        error.response?.data?.detail || "Something went wrong when creating bot"
      );
      // Handle the error (e.g., showing an error message)
    }
  };

  return (
    // <div className="w-8/12 max-w-[500px] p-5 m-auto text-white">
    <Dialog>
      <DialogTrigger className="md:tracking-widest text-base m-0 w-full text-zinc-900 ">
        新增機器人
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle></DialogTitle>
          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label htmlFor="name" className="block mb-2">
                機器人命名
              </label>
              <input
                type="text"
                id="name"
                name="name"
                value={botData.name}
                onChange={handleInputChange}
                placeholder="請用英文輸入"
                className="bg-white flex h-10 w-full items-center justify-between rounded-md border border-input px-3 py-2 ring-offset-background placeholder:text-muted-foreground disabled:cursor-not-allowed disabled:opacity-50 [&>span]:line-clamp-1"
                required
              />
            </div>
            <div className="mb-4">
              <label htmlFor="strategy" className="block mb-2">
                運行策略
              </label>
              <Select
                name="strategy"
                onValueChange={(value) => handleOptionChange(value, "strategy")}
                defaultValue="supertrend"
              >
                <SelectTrigger className="bg-inherit">
                  <SelectValue placeholder="欲運行的策略" />
                </SelectTrigger>
                <SelectContent className="">
                  {strategies.map((strategy) => (
                    <SelectItem value={strategy}>
                      {strategy.toUpperCase()}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="mb-4">
              <label htmlFor="symbol" className="block mb-2">
                交易對
              </label>
              <Select
                name="symbol"
                onValueChange={(value) => handleOptionChange(value, "symbol")}
                defaultValue="ETH/USDT"
              >
                <SelectTrigger className="bg-inherit">
                  <SelectValue placeholder="交易對" />
                </SelectTrigger>
                <SelectContent className="">
                  {symbols.map((symbol) => (
                    <SelectItem value={symbol}>{symbol}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="mb-4">
              {/* <Slider defaultValue={[33]} max={100} step={1} /> */}

              <label htmlFor="quantity" className="block mb-2">
                每次買入 (USDT)
              </label>
              <input
                type="number"
                id="quantity"
                name="quantity"
                value={botData.quantity}
                onChange={handleInputChange}
                className="flex h-10 w-full items-center justify-between rounded-md border border-input bg-inherit px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 [&>span]:line-clamp-1"
                min="11"
                max="500"
                required
              />
            </div>
            {/* <div className="mb-6">
          <label
            htmlFor="description"
            className="block text-base font-medium mb-2"
          >
            Description (Optional)
          </label>
          <textarea
            id="description"
            name="description"
            value={botData.description}
            onChange={handleInputChange}
            className="w-full p-2 rounded bg-zinc-700 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-zinc-500"
            rows={4}
          ></textarea>
        </div> */}
            <div className="flex justify-end">
              <Button type="submit">確認</Button>
            </div>
          </form>
          {/* <DialogDescription>
              This action cannot be undone. This will permanently delete your
              account and remove your data from our servers.
            </DialogDescription> */}
        </DialogHeader>
      </DialogContent>
    </Dialog>
    // </div>
  );
};

export default CreateBotForm;
