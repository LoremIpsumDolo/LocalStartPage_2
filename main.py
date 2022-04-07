from app import app, AppConfig, routes, ModuleHandler


def run_test():
    from app.utils import misc
    from rich.pretty import pprint
    from datetime import datetime
    import time

    # pprint(ModuleHandler.Modules["RaspberryModule"].DATA)
    # ModuleHandler.update_CacheData("RaspberryModule")


if __name__ == '__main__':

    ModuleHandler.update_CacheData("RedditNewsModule")

    app.run(host=AppConfig(section='flask')["host"],
            port=AppConfig(section='flask')["port"],
            debug=True,
            use_reloader=True)
