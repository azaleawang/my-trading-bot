import uvicorn
from dotenv import load_dotenv
import os
load_dotenv()  # This should be near the top of your main.py

if __name__ == "__main__":
    uvicorn.run(
        "app.app:app", host=os.getenv("HOST"), 
        port=int(os.getenv("PORT")), 
        reload=True)