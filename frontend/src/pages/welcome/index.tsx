import useCookie from "@/common/hooks/useCookie";
import { useNavigate } from "react-router-dom";

export default function Welcome() {
  const navigate = useNavigate();

  const handleImageClick = () => {
    navigate("/login");
  };
  const [username] = useCookie("username", "");
  const [access_token] = useCookie("access_token", "");
  return (
    <div className="font-sans flex flex-col flex-grow w-full h-full p-5 mt-5 pb-0 justify-center items-center space-between">
      <p className="font-bold text-slate-300 tracking-widest text-2xl lg:text-4xl mb-3">
        Hi {access_token ? username : ""} ! Welcome to
      </p>
      <p
        style={{ fontFamily: "monospace" }}
        className="font-bold text-slate-200/[80%] tracking-widest md:text-9xl	text-5xl	text-center"
      >
        AutoMate
      </p>
      <p className="font-medium text-slate-300/[60%] text-center md:mt-8 mt-5 text-2xl md:text-3xl">
        A Reliable Mate Maximizing Your Trades as You Rest
      </p>
      <div className="fixed bottom-[56px] flex gap-10">
        <img
          src="/automate.svg"
          alt="logo"
          className="hidden sm:block w-[100px]"
        />
        <img
          src="/automate.svg"
          alt="logo"
          className="w-[100px] hover:scale-110 hover:-translate-y-1 transition-transform hover:border-none"
          onClick={handleImageClick}
        />
        <img
          src="/automate.svg"
          alt="logo"
          className="hidden sm:block w-[100px]"
        />
      </div>
    </div>
  );
}
