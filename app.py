from twittor import create_app  # 不需指定__init__
app = create_app()


if __name__ == '__main__':
    app.run(debug=True)
