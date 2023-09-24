import asyncio
import uvicorn
from fapi import app

async def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    asyncio.run(main())
