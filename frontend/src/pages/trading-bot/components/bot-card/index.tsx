import { useState } from "react";

export default function BotCard() {
  const [count, setCount] = useState(0);

  return (
    <>
      <p>trading bot card</p>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
      </div>
    </>
  );
}

