module.exports = {
    apps : [{
      name: "mark-price-worker",
      script: "/home/ubuntu/trading-bot-env/bin/python3",
      args: "/home/ubuntu/my-trading-bot/backend/app/history_chart/livedata.py",
      interpreter: "", 
      time: true, 
      watch: true,
    }]
  };
  