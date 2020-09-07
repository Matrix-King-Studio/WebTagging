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

-   构建docker镜像。下载公共docker映像和安装所有必要的ubuntu包来运行项目需要一些时间。

    ```bash
    docker-compose build
    ```

-   运行docker容器。需要一些时间下载公共的镜像： postgres:10.3-alpine, redis:4.0.5-alpine 并创建容器。

    ```sh
    docker-compose up -d
    ```

-   你应该创建一个超级用户。超级用户可以使用管理面板为用户分配正确的组。

    请使用以下命令：

    ```sh
    docker exec -it cvat bash -ic 'python3 ~/manage.py createsuperuser'
    ```
    为您的管理员帐户选择登录名和密码。欲了解更多信息，请阅读 [Django documentation](https://docs.djangoproject.com/en/2.2/ref/django-admin/#createsuperuser).

-   模型的迁移与同步。

    请使用以下命令：

    ```sh
    docker exec -it cvat bash -ic 'python3 ~/manage.py makemigrations'
    docker exec -it cvat bash -ic 'python3 ~/manage.py migrate'
    ```
