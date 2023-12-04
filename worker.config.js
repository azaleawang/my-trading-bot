module.exports = {
    apps : [{
      name: "trading-bot-monitor",
      script: "/home/ubuntu/trading-bot-env/bin/python3",
      args: "/home/ubuntu/my-trading-bot/backend/docker-worker/monitor.py",
      interpreter: "", 
      time: true, 
      watch: true,
    }]
  };
  