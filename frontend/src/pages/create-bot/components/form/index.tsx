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
import { Plus, PlusCircle, PlusSquare } from "lucide-react";

const CreateBotForm: React.FC = () => {
  const navigate = useNavigate();
  const [userId] = useCookie("user_id", "");
  const [access_token] = useCookie("access_token", "");
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
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
    setBotData({ ...botData, [e.target.name]: e.target.value?.trim() });
  };

  // function debounce(fn: any, delay = 500) {
  //   let timer: any;

  //   // debounce function 最終會回傳一個 function
  //   return (...args: any) => {
  //     // 每一次 debounce function 被觸發時，會先清除之前的 timer，避免觸發先前的 fn 函式
  //     // 因此只要在 delay 時間內觸發 debounce function，就會一直清除先前的 timer，避免 fn 一直被執行
  //     clearTimeout(timer);
  //     // 清除之後，再重新計時
  //     // 當 delay 時間到時，執行 fn
  //     timer = setTimeout(() => {
  //       fn(...args);
  //     }, delay);
  //   };
  // }

  // updateDebounceText 會在延遲 500 ms 後執行 console.log('call api get search result')

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    const nameRegex = /^[A-Za-z-_1234567890]+$/; // Only accept -,_ and alphabets
    if (!nameRegex.test(botData.name)) {
      toast.warn("名稱欄位僅接受英文數字以及連字號 🙌");
      return;
    }

    if (botData.name.trim().length > 20 || botData.name.trim().length < 3) {
      toast.warn("名稱字數需介於3~20字 🙌");
      return;
    }

    const submissionData = {
      ...botData,
      owner_id: Number(userId),
      created_at: new Date().toISOString(),
    };

    try {
      setIsSubmitting(true);
      console.log(submissionData);
      const response = await axios.post(
        `${bot_api_base(undefined)}/`,
        submissionData,
        {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        }
      );
      console.log(response.data);
      if (
        confirm(
          `機器人 ${response.data.data.name} 已創建! 交易對: ${response.data.data.symbol}`
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
    } finally {
      setIsSubmitting(false);
    }
  };

  // const debouncedSubmit = debounce(handleSubmit);
  // const handleFormSubmit = (e: React.FormEvent<HTMLFormElement>) => {
  //   e.preventDefault(); // 在这里调用 preventDefault
  //   debouncedSubmit();   // 然后调用防抖函数
  // };

  return (
    // <div className="w-8/12 max-w-[500px] p-5 m-auto text-white">
    <Dialog>
      <DialogTrigger className="md:tracking-widest text-base m-0 w-full flex items-center justify-center gap-2">
        {/* <PlusSquare size={28} /> */}
        <Plus size={20} /> 機器人
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
            <div className="flex justify-end">
              <Button type="submit" disabled={isSubmitting}>
                確認
              </Button>
            </div>
          </form>
        </DialogHeader>
      </DialogContent>
    </Dialog>
    // </div>
  );
};

export default CreateBotForm;
