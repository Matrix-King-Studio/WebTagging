- [快速安装指南](#快速安装指南)
  - [Ubuntu 18.04 (x86_64/amd64)](#ubuntu-1804-x86_64amd64)

# 快速安装指南

## Ubuntu 18.04 (x86_64/amd64)
-   打开终端窗口。

-   在终端窗口中键入以下命令以安装`docker`。

    ```sh
    sudo apt-get update
    sudo apt-get --no-install-recommends install -y \
      apt-transport-https \
      ca-certificates \
      curl \
      gnupg-agent \
      software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository \
      "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) \
      stable"
    sudo apt-get update
    sudo apt-get --no-install-recommends install -y docker-ce docker-ce-cli containerd.io
    ```

-   参考 [post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/) 在没有root权限的情况下运行docker。

    ```sh
    sudo groupadd docker
    sudo usermod -aG docker $USER
    ```
    注销并重新登录（或重新启动），以便重新评估组成员身份。

    然后，您可以在终端窗口中键入`groups`命令，并检查`docker`group是否在其输出中。

-   安装 docker-compose (≥1.19.0).

    Compose是一个用于定义和运行多容器docker应用程序的工具。

    ```bash
    sudo apt-get --no-install-recommends install -y python3-pip
    sudo python3 -m pip install setuptools docker-compose
    ```

-   克隆项目源代码从[GitHub repository](https://github.com/Matrix-King-Studio/WebTagging).

    ```bash
    sudo apt-get --no-install-recommends install -y git
    git clone https://github.com/Matrix-King-Studio/WebTagging.git
    cd WebTagging
    ```

-   Build docker images by default. It will take some time to download public
    docker image ubuntu:16.04 and install all necessary ubuntu packages to run
    CVAT server.

    ```bash
    docker-compose build
    ```

-   Run docker containers. It will take some time to download public docker
    images like postgres:10.3-alpine, redis:4.0.5-alpine and create containers.

    ```sh
    docker-compose up -d
    ```

-   You can register a user but by default it will not have rights even to view
    list of tasks. Thus you should create a superuser. A superuser can use an
    admin panel to assign correct groups to the user. Please use the command
    below:

    ```sh
    docker exec -it cvat bash -ic 'python3 ~/manage.py createsuperuser'
    ```
    Choose login and password for your admin account. For more information
    please read [Django documentation](https://docs.djangoproject.com/en/2.2/ref/django-admin/#createsuperuser).

-   Google Chrome is the only browser which is supported by CVAT. You need to
    install it as well. Type commands below in a terminal window:

    ```sh
    curl https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
    sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
    sudo apt-get update
    sudo apt-get --no-install-recommends install -y google-chrome-stable
    ```

-   Open the installed Google Chrome browser and go to [localhost:8080](http://localhost:8080).
    Type your login/password for the superuser on the login page and press the _Login_
    button. Now you should be able to create a new annotation task. Please read the
    [CVAT user's guide](/cvat/apps/documentation/user_guide.md) for more details.
