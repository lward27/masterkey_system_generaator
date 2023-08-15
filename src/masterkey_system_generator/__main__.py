import uvicorn
from masterkey_system_generator.api import app

def main():
    uvicorn.run(app, host='0.0.0.0')

if __name__ == "__main__":
    main()