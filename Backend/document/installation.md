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

- Clone _CVAT_ source code from the [GitHub repository](https://github.com/Matrix-King-Studio/WebTagging).

  ```bash
  sudo apt-get --no-install-recommends install -y git
  git clone https://github.com/Matrix-King-Studio/WebTagging.git
  cd WebTagging/Backend
  ```

- Build docker images by default.

  ```bash
  docker-compose build
  ```

- Run docker containers.

  ```sh
  docker-compose up -d
  ```

- 注册超级用户

  ```sh
  docker exec -it cvat bash -ic 'python3 ~/manage.py createsuperuser'
  ```

- 安装 Google Chrome 支持

  ```sh
  curl https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
  sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
  sudo apt-get update
  sudo apt-get --no-install-recommends install -y google-chrome-stable
  ```

- 访问：http://{ IP }:8080/admin/

## Advanced Topics

### Additional components

- [Analytics: management and monitoring of data annotation team](/components/analytics/README.md)

```bash
# Build and run containers with Analytics component support:
docker-compose -f docker-compose.yml -f components/analytics/docker-compose.analytics.yml up -d --build
```

### （半）自动标注

Please follow [instructions](/document/installation_automatic_annotation.md)

### 暂停所有容器

下面的 command 会停止并删除 `up` 创建的 containers, networks, volumes, and images.

```bash
docker-compose down
```

### Share path

在创建任务期间，可以使用共享存储上载数据。

```yml
version: '3.3'

services:
  cvat:
    environment:
      CVAT_SHARE_URL: 'Mounted from /mnt/share host directory'
    volumes:
      - cvat_share:/home/django/share:ro

volumes:
  cvat_share:
    driver_opts:
      type: none
      device: /mnt/share
      o: bind
```

### Email verification

You can enable email verification for newly registered users.
Specify these options in the [settings file](../../settings/base.py) to configure Django allauth
to enable email verification (ACCOUNT_EMAIL_VERIFICATION = 'mandatory').
Access is denied until the user's email address is verified.

```python
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

# Email backend settings for Django
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
```

Also you need to configure the Django email backend to send emails.
This depends on the email server you are using and is not covered in this tutorial, please see
[Django SMTP backend configuration](https://docs.djangoproject.com/en/3.1/topics/email/#django.core.mail.backends.smtp.EmailBackend)
for details.
