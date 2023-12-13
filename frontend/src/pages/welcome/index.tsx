import { useNavigate } from "react-router-dom";

export default function Welcome() {
  const navigate = useNavigate();

  const handleImageClick = () => {
    navigate("/login");
  };

  return (
    <div className="flex flex-col flex-grow w-full h-full p-5 mt-5 pb-0 justify-center items-center space-between">
      <p
        style={{ fontSize: "120px", fontFamily: "monospace" }}
        className="font-bold text-slate-200/[80%] tracking-widest"
      >
        AutoMate
      </p>
      <p
        style={{ fontSize: "30px", fontFamily: "sans-serif" }}
        className="font-medium text-slate-300/[60%] lg:w-2/3 text-center"
      >
        A Reliable Mate Maximizing Your Trades as You Rest
      </p>
      <div className="fixed bottom-[56px] flex gap-10">
        <img src="src/assets/automate.svg" alt="logo" className="w-[100px]" />
        <img
          src="src/assets/automate.svg"
          alt="logo"
          className="w-[100px] hover:scale-110 hover:-translate-y-1 transition-transform hover:border-none"
          onClick={handleImageClick} 
        />
        <img src="src/assets/automate.svg" alt="logo" className="w-[100px]" />
      </div>
    </div>
  );
}
