from app import app, AppConfig, routes

if __name__ == '__main__':

    app.run(host=AppConfig(section='flask')["host"],
            port=AppConfig(section='flask')["port"],
            debug=True,
            use_reloader=True)
