<div align="center">
  <div>
    <img width="100" alt="homepage" src="https://github.com/azaleawang/my-trading-bot/assets/46614777/cc29fcb0-c1a2-44ca-8a87-e8e72a4e9bab"> 
    <h1>AutoMate</h1>
  </div>
  <strong>A platform providing long-term script execution and strategy backtesting tools for crypto traders.</strong>
  <div align="center">
    <a href="https://azaleasites.online/">Home</a>

</div>
</div>

## Table of Content

* [Tech Stack](#tech-stack)
* [Architecture and Main Features](#architecture-and-main-features)
* [Demo Video](#demo-video)
* [Demo account](#demo-account)
  
## Tech Stack

### Back-End

![FastAPI](https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white)
![python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=ble&color=white)
![docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white)
![pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)
![ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)

### Cloud Service

![Amazon_AWS](https://img.shields.io/badge/Amazon%20AWS-232F3E.svg?style=for-the-badge&logo=Amazon-AWS&logoColor=white)

* EC2 / RDS / ElastiCache / Lambda / SQS / S3 / AMI / CloudWatch

### Front-End

![Typescript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![ReactRouter](https://img.shields.io/badge/React_Router-CA4245?style=for-the-badge&logo=react-router&logoColor=white)
![Tailwind](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![shadcn](https://img.shields.io/badge/shadcn/ui-000000.svg?style=for-the-badge&logo=shadcn/ui&logoColor=white)
![Vite](https://img.shields.io/badge/vite-%23646CFF.svg?style=for-the-badge&logo=vite&logoColor=white)

### Database

![postgresql](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![redis](https://img.shields.io/badge/redis-%23DD0031.svg?&style=for-the-badge&logo=redis&logoColor=white)
![InfluxDB](https://img.shields.io/badge/InfluxDB-22ADF6?style=for-the-badge&logo=InfluxDB&logoColor=white)

### Third-Party API

![binance](https://img.shields.io/badge/Binance-FCD535?style=for-the-badge&logo=binance&logoColor=white)

### Tools

![ORM](https://img.shields.io/badge/SQLAlchemy-D71F00.svg?style=for-the-badge&logo=SQLAlchemy&logoColor=white)
![pydantic](https://img.shields.io/badge/Pydantic-E92063.svg?style=for-the-badge&logo=Pydantic&logoColor=white)
![GIT](https://img.shields.io/badge/GIT-E44C30?style=for-the-badge&logo=git&logoColor=white)
![GitHub_Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![pytest](https://img.shields.io/badge/Pytest-0A9EDC.svg?style=for-the-badge&logo=Pytest&logoColor=white)
![swagger](https://img.shields.io/badge/Swagger-85EA2D.svg?style=for-the-badge&logo=Swagger&logoColor=black)

### Networking

* HTTPS
* WebSocket
* Domain Name System (DNS)

### CICD

* Automated deployment on AWS EC2 using GitHub Actions CI/CD.

## Architecture and Main Features

### Overview

<div align="center">
    <img src="https://github.com/azaleawang/my-trading-bot/assets/46614777/94787b69-acde-4356-bc92-cc816651be9a" alt="overview">
</div>

### Scalable Trading Bot

* Implemented the deployment of trading bot scripts within isolated Docker containers.

* Implemented a [bot worker server](https://github.com/azaleawang/my-trading-bot-worker) to handle high RAM usage of trading bot, offloading the resources from main server.
* Utilized AWS AMI for rapidly scaling worker servers.
* Engineered a bot management system handled by the main server, facilitating communication between the worker and main servers to optimize server utilization and idle time.
* Established a regular collection of trading bot running statuses on worker servers, providing information on operational health.
* Employed WebSocket to enable trade real-time notifications and data transmission to the main server.

<div align="center">
    <img src="https://github.com/azaleawang/my-trading-bot/assets/46614777/cc25173a-5244-4f20-9b43-455775d1d6a4" alt="overview">
</div>

### Real-time Mark Price Processing

* Developed a worker for real-time mark price streaming with Binanca WebSocket API.
* Utilized InfluxDB for time-series data storage, aiding in real-time calculations of unrealized profits of trading bot.

<div align="center">
    <img src="https://github.com/azaleawang/my-trading-bot/assets/46614777/2714e5ce-a4e0-49aa-890e-85bc9a00489c" alt="livedata">
</div>

### Serverless Computation of Strategy Backtesting

:octocat: [My code](https://github.com/azaleawang/strategy-backtesting-lambda)

* Utilized the Python `Backtesting.py` and `CCXT` API packages for history data retrieval and strategy backtesting.
* Containerized Python environment specifically for backtesting using Docker image.
* Deployed the containerized backtesting tasks within AWS Lambda, efficiently handling the high computational demands.

<div align="center">
    <img src="https://github.com/azaleawang/my-trading-bot/assets/46614777/dc200d52-e2c3-45b0-826d-8c2919244978" alt="backtesting">
</div>

## Demo Video

### Trading bot

<https://github.com/azaleawang/my-trading-bot/assets/46614777/921267d8-6d1c-4786-8a82-fc383ebe9df8>

### Strategy backtesting

<https://github.com/azaleawang/my-trading-bot/assets/46614777/6bd22e66-ce44-47ed-a3e5-7773d1c95e25>

## Demo Account

| Email         | Password |
| ------------- | -------- |
| <test@test.com> | string   |
