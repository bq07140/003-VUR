# -*- coding: utf-8 -*-
from fhApp import create_app
from config import ProjectConfig
import platform

os_name = platform.system()


app = create_app(ProjectConfig['mode'])


if __name__ == '__main__':

    print(app.url_map)
    print(os_name)

    if os_name == "Windows":
        app.run(host=ProjectConfig['host'],
                port=ProjectConfig['port'],
                processes=1)

    elif os_name == "Linux":
        app.run(host=ProjectConfig['host'],
                port=ProjectConfig['port'],
                processes=ProjectConfig['processes'],
                threaded=False)



