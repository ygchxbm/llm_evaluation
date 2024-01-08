from app import create_app

app = create_app()

if __name__ == "__main__":
    # 仅仅直接python main.py运行的时候才会通过这里启动服务器
    app.run(host="0.0.0.0", port=5000, debug=True)