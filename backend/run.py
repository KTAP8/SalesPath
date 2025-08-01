from app import create_app
import os
app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"⚡ Starting backend on port {port}")
    app.run(host="0.0.0.0", port=port)
