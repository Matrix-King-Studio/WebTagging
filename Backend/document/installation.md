# Quick installation backend guide

## Ubuntu 18.04 (x86_64/amd64)

- 打开 Terminal

- 在 Terminal 输入以下命令安装 `docker`.

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

- 执行 [post-installation steps](https://docs.docker.com/install/linux/linux-postinstall/) 以在没有权限的情况下运行 docker

  ```sh
  sudo groupadd docker
  sudo usermod -aG docker $USER
  ```

- 安装 docker-compose (1.19.0 or newer)

  ```bash
  sudo apt-get --no-install-recommends install -y python3-pip python3-setuptools
  sudo python3 -m pip install setuptools docker-compose
  ```

- Clone project source code [GitHub repository](https://github.com/Matrix-King-Studio/WebTagging).

  ```bash
  sudo apt-get --no-install-recommends install -y git
  git clone https://github.com/Matrix-King-Studio/WebTagging.git
  cd WebTagging/Backend
  sudo mkdir /mnt/share
  ```

- Build docker images by default.

  ```bash
  docker-compose build
  ```

- Run docker containers.

  ```sh
  docker-compose up -d
  ```

- 数据库迁移

    ```shell
    docker exec -it cvat bash -ic 'python3 ~/manage.py makemigrations'
    docker exec -it cvat bash -ic 'python3 ~/manage.py migrate'
    ```

- 注册超级用户

  ```sh
  docker exec -it cvat bash -ic 'python3 ~/manage.py createsuperuser'
  ```

- 访问：http://{ IP }:8080/admin/

- 停止运行所有容器

  ```sh
  docker stop $(docker ps -aq)
  ```
