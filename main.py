import uvicorn
import ssl

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host='0.0.0.0',
        port=8000,
        reload=True,
        ssl_version=ssl.PROTOCOL_SSLv23,
        ssl_keyfile="key.pem",
        ssl_certfile="cert.pem"
    )