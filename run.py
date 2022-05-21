from uvicorn.main import run


if __name__ == '__main__':
    # import
    from service.app import create_app
    from service.config import HOST, PORT

    # instatiate the app
    app = create_app()

    # run the app
    run(app=app, host=HOST, port=PORT)
