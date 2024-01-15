import uvicorn
from dotenv import load_dotenv
import os
from app.utils.logger import setup_logger

load_dotenv()
setup_logger()

if __name__ == "__main__":
    uvicorn.run(
        "app.app:app", host="0.0.0.0", 
        port=int(os.getenv("PORT")), 
        reload=True)