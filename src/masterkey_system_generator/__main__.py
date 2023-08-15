import uvicorn
from masterkey_system_generator.api import app

def main():
    uvicorn.run(app)

if __name__ == "__main__":
    main()