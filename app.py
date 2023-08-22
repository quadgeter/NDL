from website import createApp
import os

app = createApp()

if __name__ == "__main__":
    app.run(port=os.environ.get("PORT", 8080))