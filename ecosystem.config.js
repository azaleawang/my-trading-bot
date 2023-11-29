module.exports = {
    apps : [{
      name: "my-trading-bot",
      script: "/home/ubuntu/trading-bot-env/bin/python3",
      args: "/home/ubuntu/my-trading-bot/backend/main.py",
      interpreter: "", 
      watch: true,
    }]
  };
  