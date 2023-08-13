

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Installing Elasticsearch](install-
elasticsearch.md)

[« Install Elasticsearch with RPM](rpm.md) [Run Elasticsearch locally
»](run-elasticsearch-locally.md)

## 使用 Docker 安装 Elasticsearch

Elasticsearch也可以作为Docker镜像使用。atwww.docker.elastic.co 提供了所有已发布的 Docker 映像和标记的列表。源文件位于 Github 中。

此软件包包含免费和订阅功能。开始 30 天试用以试用所有功能。

从 Elasticsearch 8.0 开始，默认情况下启用安全性。启用安全性后，Elastic Stack 安全功能需要对传输网络层进行 TLS 加密，否则您的集群将无法启动。

### 安装 Docker Desktop 或 DockerEngine

为您的操作系统安装相应的 Docker 应用程序。

确保为 Docker 分配了至少 4GiB 的内存。在 Docker 桌面版中，您可以在首选项 (macOS) 或设置 (Windows) 中的"高级"选项卡上配置资源使用情况。

### 拉取 Elasticsearch Dockerimage

获取 Elasticsearch for Docker 就像对 Elastic Docker 注册表发出"docker pull"命令一样简单。

    
    
    docker pull docker.elastic.co/elasticsearch/elasticsearch:8.9.0

### 可选：验证 Elasticsearch Docker 镜像签名

尽管它是可选的，但我们强烈建议验证下载的 Docker 映像中包含的签名，以确保映像有效。

弹性映像使用Cosign签名，Cosign是Sigstore项目的一部分。

Cosign 支持容器签名、验证和存储在 OCIregistry 中。

为您的操作系统安装相应的 Cosign应用程序。

Elasticsearch v8.9.0 的容器镜像签名可以按如下方式验证：

    
    
    wget https://artifacts.elastic.co/cosign.pub __cosign verify --key cosign.pub docker.elastic.co/elasticsearch/elasticsearch:8.9.0 __

__

|

下载弹性公有密钥以验证容器签名 ---|--- __

|

根据弹性公有密钥验证容器 该命令以 JSON 格式打印检查结果和签名有效负载：

    
    
    Verification for docker.elastic.co/elasticsearch/elasticsearch:{version} --
    The following checks were performed on each of these signatures:
      - The cosign claims were validated
      - Existence of the claims in the transparency log was verified offline
      - The signatures were verified against the specified public key

现在您已经验证了 Elasticsearch Docker 镜像签名，您可以启动单节点或多节点集群。

### 使用 Docker 启动单节点群集

如果您在 Docker 容器中启动单节点 Elasticsearch 集群，系统将自动为您启用和配置安全性。首次启动 Elasticsearch 时，会自动进行以下安全配置：

* 为传输层和 HTTP 层生成证书和密钥。  * 传输层安全性 (TLS) 配置设置写入"elasticsearch.yml"。  * 为"弹性"用户生成密码。  * 将为 Kibana 生成注册令牌。

然后，您可以启动 Kibana 并输入注册令牌，该令牌的有效期为 30 分钟。此令牌会自动应用来自 Elasticsearch 集群的安全设置，使用 'kibana_system' 用户向 Elasticsearch 进行身份验证，并将安全配置写入 'kibana.yml'。

以下命令启动单节点 Elasticsearch 集群进行开发或测试。

1. 为 Elasticsearch 创建新的 docker 网络，Kibana docker 网络创建弹性

2. 在 Docker 中启动 Elasticsearch。将为"弹性"用户生成一个密码并输出到终端，以及用于注册 Kibana 的注册令牌。           Docker run --name es01 --net elastic -p 9200：9200 -it docker.elastic.co/elasticsearch/elasticsearch:8.9.0

您可能需要在终端中向后滚动一点才能查看密码和注册令牌。

3. 复制生成的密码和注册令牌，并将其保存在安全位置。这些值仅在您第一次启动 Elasticsearch 时显示。

如果您需要重置"弹性"用户或其他内置用户的密码，请运行"弹性搜索重置密码"工具。此工具位于 Docker 容器的 Elasticsearch '/bin' 目录中。例如：

    
        docker exec -it es01 /usr/share/elasticsearch/bin/elasticsearch-reset-password

4. 将"http_ca.crt"安全证书从 Docker 容器复制到本地计算机。           Docker cp es01：/usr/share/elasticsearch/config/certs/http_ca.crt .

5. 打开一个新终端，并使用从 Docker 容器复制的"http_ca.crt"文件，验证您是否可以通过进行经过身份验证的调用来连接到 Elasticsearch 集群。出现提示时，输入"弹性"用户的密码。           卷曲 --cacert http_ca.crt -u 弹性 https://localhost:9200

### 注册其他节点

首次启动 Elasticsearch 时，安装过程默认配置单节点集群。此过程还会生成注册令牌并将其打印到终端。如果希望节点加入现有群集，请使用生成的注册令牌启动新节点。

**生成注册令牌**

注册令牌的有效期为 30 分钟。如果需要生成新注册令牌，请在现有节点上运行"弹性搜索-创建-注册令牌"工具。此工具位于 Docker 容器的 Elasticsearch 'bin' 目录中。

例如，在现有的"es01"节点上运行以下命令，为新的 Elasticsearch 节点生成注册令牌：

    
    
    docker exec -it es01 /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s node

1. 在您启动第一个节点的终端中，复制生成的注册令牌以添加新的 Elasticsearch 节点。  2. 在新节点上，启动 Elasticsearch 并包含生成的注册令牌。           docker run -e ENROLLMENT_TOKEN="" --<token>name es02 --net elastic -it docker.elastic.co/elasticsearch/elasticsearch:8.9.0

Elasticsearch 现在配置为加入现有集群。

#### 设置 JVM 堆大小

如果在第二个节点启动时遇到第一个节点所在的容器退出的问题，请显式设置 JVM 堆大小的值。要手动配置堆大小，请包括"ES_JAVA_OPTS"变量，并在启动每个节点时设置"-Xms"和"-Xmx"的值。例如，以下命令启动节点 'es02' 并将最小和最大 JVM 堆大小设置为 1 GB：

    
    
    docker run -e ES_JAVA_OPTS="-Xms1g -Xmx1g" -e ENROLLMENT_TOKEN="<token>" --name es02 -p 9201:9200 --net elastic -it docker.elastic.co/elasticsearch/elasticsearch:8.9.0

#### 后续步骤

您现在已经设置了一个测试Elasticsearch环境。在开始使用 Elasticsearch 进行认真开发或投入生产之前，请查看在 Docker 正式生产环境中运行 Elasticsearch 时要应用的要求和建议。

#### 安全证书和密钥

安装 Elasticsearch 时，会在 Elasticsearch 配置目录中生成以下证书和密钥，用于将 Kibana 实例连接到安全的 Elasticsearch 集群并加密节点间通信。此处列出了这些文件以供参考。

`http_ca.crt`

     The CA certificate that is used to sign the certificates for the HTTP layer of this Elasticsearch cluster. 
`http.p12`

     Keystore that contains the key and certificate for the HTTP layer for this node. 
`transport.p12`

     Keystore that contains the key and certificate for the transport layer for all the nodes in your cluster. 

'http.p12' 和 'transport.p12' 是受密码保护的 PKCS#12 密钥库。Elasticsearch 将这些密钥库的密码存储为 securesettings。要检索密码以便检查或更改密钥库内容，请使用"bin/elasticsearch-keystore"工具。

使用以下命令检索"http.p12"的密码：

    
    
    bin/elasticsearch-keystore show xpack.security.http.ssl.keystore.secure_password

使用以下命令检索"transport.p12"的密码：

    
    
    bin/elasticsearch-keystore show xpack.security.transport.ssl.keystore.secure_password

### 使用 DockerCompose 启动多节点集群

要在启用安全性的情况下在 Docker 中启动并运行多节点 Elasticsearch 集群和 Kibana，您可以使用 Docker Compose。

此配置提供了一种启动安全群集的简单方法，您可以在构建具有多个主机的分布式部署之前使用该群集进行开发。

####Prerequisites

为您的操作系统安装相应的 Docker 应用程序。

如果你在 Linux 上运行，请安装 DockerCompose。

确保为 Docker 分配了至少 4GB 的内存。在 Docker Desktop 中，您可以在首选项 (macOS) 或设置 (Windows) 中的"高级"选项卡上配置资源使用情况。

#### 准备环境

在新的空目录中创建以下配置文件。这些文件也可以从GitHub上的theelasticsearchrepository获得。

######'.env'

".env"文件设置运行"docker-compose.yml"配置文件时使用的环境变量。确保使用"ELASTIC_PASSWORD"和"KIBANA_PASSWORD"变量为"弹性"和"kibana_system"用户指定强密码。这些变量由"docker-compose.yml"文件引用。

您的密码必须是字母数字，并且不能包含特殊字符，例如"！"或"@"。'docker-compose.yml'文件中包含的"bash"脚本仅对字母数字字符进行操作。

    
    
    # Password for the 'elastic' user (at least 6 characters)
    ELASTIC_PASSWORD=
    
    # Password for the 'kibana_system' user (at least 6 characters)
    KIBANA_PASSWORD=
    
    # Version of Elastic products
    STACK_VERSION=8.9.0
    
    # Set the cluster name
    CLUSTER_NAME=docker-cluster
    
    # Set to 'basic' or 'trial' to automatically start the 30-day trial
    LICENSE=basic
    #LICENSE=trial
    
    # Port to expose Elasticsearch HTTP API to the host
    ES_PORT=9200
    #ES_PORT=127.0.0.1:9200
    
    # Port to expose Kibana to the host
    KIBANA_PORT=5601
    #KIBANA_PORT=80
    
    # Increase or decrease based on the available host memory (in bytes)
    MEM_LIMIT=1073741824
    
    # Project namespace (defaults to the current folder name if not set)
    #COMPOSE_PROJECT_NAME=myproject

##### 'docker-compose.yml'

这个'docker-compose.yml'文件创建了一个启用了身份验证和网络加密的三节点安全Elasticsearchcluster，以及一个安全地连接到它的Kibanainstance。

**公开端口**

此配置在所有网络接口上公开端口"9200"。由于 Docker 处理端口的方式，未绑定到"localhost"的端口会让您的 Elasticsearch 集群可公开访问，从而可能忽略任何防火墙设置。如果不想向外部主机公开端口"9200"，请将".env"文件中"ES_PORT"的值设置为类似于"127.0.0.1：9200"。然后，Elasticsearch只能从主机本身访问。

    
    
    version: "2.2"
    
    services:
      setup:
        image: docker.elastic.co/elasticsearch/elasticsearch:${STACK_VERSION}
        volumes:
          - certs:/usr/share/elasticsearch/config/certs
        user: "0"
        command: >
          bash -c '
            if [ x${ELASTIC_PASSWORD} == x ]; then
              echo "Set the ELASTIC_PASSWORD environment variable in the .env file";
              exit 1;
            elif [ x${KIBANA_PASSWORD} == x ]; then
              echo "Set the KIBANA_PASSWORD environment variable in the .env file";
              exit 1;
            fi;
            if [ ! -f config/certs/ca.zip ]; then
              echo "Creating CA";
              bin/elasticsearch-certutil ca --silent --pem -out config/certs/ca.zip;
              unzip config/certs/ca.zip -d config/certs;
            fi;
            if [ ! -f config/certs/certs.zip ]; then
              echo "Creating certs";
              echo -ne \
              "instances:\n"\
              "  - name: es01\n"\
              "    dns:\n"\
              "      - es01\n"\
              "      - localhost\n"\
              "    ip:\n"\
              "      - 127.0.0.1\n"\
              "  - name: es02\n"\
              "    dns:\n"\
              "      - es02\n"\
              "      - localhost\n"\
              "    ip:\n"\
              "      - 127.0.0.1\n"\
              "  - name: es03\n"\
              "    dns:\n"\
              "      - es03\n"\
              "      - localhost\n"\
              "    ip:\n"\
              "      - 127.0.0.1\n"\
              > config/certs/instances.yml;
              bin/elasticsearch-certutil cert --silent --pem -out config/certs/certs.zip --in config/certs/instances.yml --ca-cert config/certs/ca/ca.crt --ca-key config/certs/ca/ca.key;
              unzip config/certs/certs.zip -d config/certs;
            fi;
            echo "Setting file permissions"
            chown -R root:root config/certs;
            find . -type d -exec chmod 750 \{\} \;;
            find . -type f -exec chmod 640 \{\} \;;
            echo "Waiting for Elasticsearch availability";
            until curl -s --cacert config/certs/ca/ca.crt https://es01:9200 | grep -q "missing authentication credentials"; do sleep 30; done;
            echo "Setting kibana_system password";
            until curl -s -X POST --cacert config/certs/ca/ca.crt -u "elastic:${ELASTIC_PASSWORD}" -H "Content-Type: application/json" https://es01:9200/_security/user/kibana_system/_password -d "{\"password\":\"${KIBANA_PASSWORD}\"}" | grep -q "^{}"; do sleep 10; done;
            echo "All done!";
          '
        healthcheck:
          test: ["CMD-SHELL", "[ -f config/certs/es01/es01.crt ]"]
          interval: 1s
          timeout: 5s
          retries: 120
    
      es01:
        depends_on:
          setup:
            condition: service_healthy
        image: docker.elastic.co/elasticsearch/elasticsearch:${STACK_VERSION}
        volumes:
          - certs:/usr/share/elasticsearch/config/certs
          - esdata01:/usr/share/elasticsearch/data
        ports:
          - ${ES_PORT}:9200
        environment:
          - node.name=es01
          - cluster.name=${CLUSTER_NAME}
          - cluster.initial_master_nodes=es01,es02,es03
          - discovery.seed_hosts=es02,es03
          - ELASTIC_PASSWORD=${ELASTIC_PASSWORD}
          - bootstrap.memory_lock=true
          - xpack.security.enabled=true
          - xpack.security.http.ssl.enabled=true
          - xpack.security.http.ssl.key=certs/es01/es01.key
          - xpack.security.http.ssl.certificate=certs/es01/es01.crt
          - xpack.security.http.ssl.certificate_authorities=certs/ca/ca.crt
          - xpack.security.transport.ssl.enabled=true
          - xpack.security.transport.ssl.key=certs/es01/es01.key
          - xpack.security.transport.ssl.certificate=certs/es01/es01.crt
          - xpack.security.transport.ssl.certificate_authorities=certs/ca/ca.crt
          - xpack.security.transport.ssl.verification_mode=certificate
          - xpack.license.self_generated.type=${LICENSE}
        mem_limit: ${MEM_LIMIT}
        ulimits:
          memlock:
            soft: -1
            hard: -1
        healthcheck:
          test:
            [
              "CMD-SHELL",
              "curl -s --cacert config/certs/ca/ca.crt https://localhost:9200 | grep -q 'missing authentication credentials'",
            ]
          interval: 10s
          timeout: 10s
          retries: 120
    
      es02:
        depends_on:
          - es01
        image: docker.elastic.co/elasticsearch/elasticsearch:${STACK_VERSION}
        volumes:
          - certs:/usr/share/elasticsearch/config/certs
          - esdata02:/usr/share/elasticsearch/data
        environment:
          - node.name=es02
          - cluster.name=${CLUSTER_NAME}
          - cluster.initial_master_nodes=es01,es02,es03
          - discovery.seed_hosts=es01,es03
          - bootstrap.memory_lock=true
          - xpack.security.enabled=true
          - xpack.security.http.ssl.enabled=true
          - xpack.security.http.ssl.key=certs/es02/es02.key
          - xpack.security.http.ssl.certificate=certs/es02/es02.crt
          - xpack.security.http.ssl.certificate_authorities=certs/ca/ca.crt
          - xpack.security.transport.ssl.enabled=true
          - xpack.security.transport.ssl.key=certs/es02/es02.key
          - xpack.security.transport.ssl.certificate=certs/es02/es02.crt
          - xpack.security.transport.ssl.certificate_authorities=certs/ca/ca.crt
          - xpack.security.transport.ssl.verification_mode=certificate
          - xpack.license.self_generated.type=${LICENSE}
        mem_limit: ${MEM_LIMIT}
        ulimits:
          memlock:
            soft: -1
            hard: -1
        healthcheck:
          test:
            [
              "CMD-SHELL",
              "curl -s --cacert config/certs/ca/ca.crt https://localhost:9200 | grep -q 'missing authentication credentials'",
            ]
          interval: 10s
          timeout: 10s
          retries: 120
    
      es03:
        depends_on:
          - es02
        image: docker.elastic.co/elasticsearch/elasticsearch:${STACK_VERSION}
        volumes:
          - certs:/usr/share/elasticsearch/config/certs
          - esdata03:/usr/share/elasticsearch/data
        environment:
          - node.name=es03
          - cluster.name=${CLUSTER_NAME}
          - cluster.initial_master_nodes=es01,es02,es03
          - discovery.seed_hosts=es01,es02
          - bootstrap.memory_lock=true
          - xpack.security.enabled=true
          - xpack.security.http.ssl.enabled=true
          - xpack.security.http.ssl.key=certs/es03/es03.key
          - xpack.security.http.ssl.certificate=certs/es03/es03.crt
          - xpack.security.http.ssl.certificate_authorities=certs/ca/ca.crt
          - xpack.security.transport.ssl.enabled=true
          - xpack.security.transport.ssl.key=certs/es03/es03.key
          - xpack.security.transport.ssl.certificate=certs/es03/es03.crt
          - xpack.security.transport.ssl.certificate_authorities=certs/ca/ca.crt
          - xpack.security.transport.ssl.verification_mode=certificate
          - xpack.license.self_generated.type=${LICENSE}
        mem_limit: ${MEM_LIMIT}
        ulimits:
          memlock:
            soft: -1
            hard: -1
        healthcheck:
          test:
            [
              "CMD-SHELL",
              "curl -s --cacert config/certs/ca/ca.crt https://localhost:9200 | grep -q 'missing authentication credentials'",
            ]
          interval: 10s
          timeout: 10s
          retries: 120
    
      kibana:
        depends_on:
          es01:
            condition: service_healthy
          es02:
            condition: service_healthy
          es03:
            condition: service_healthy
        image: docker.elastic.co/kibana/kibana:${STACK_VERSION}
        volumes:
          - certs:/usr/share/kibana/config/certs
          - kibanadata:/usr/share/kibana/data
        ports:
          - ${KIBANA_PORT}:5601
        environment:
          - SERVERNAME=kibana
          - ELASTICSEARCH_HOSTS=https://es01:9200
          - ELASTICSEARCH_USERNAME=kibana_system
          - ELASTICSEARCH_PASSWORD=${KIBANA_PASSWORD}
          - ELASTICSEARCH_SSL_CERTIFICATEAUTHORITIES=config/certs/ca/ca.crt
        mem_limit: ${MEM_LIMIT}
        healthcheck:
          test:
            [
              "CMD-SHELL",
              "curl -s -I http://localhost:5601 | grep -q 'HTTP/1.1 302 Found'",
            ]
          interval: 10s
          timeout: 10s
          retries: 120
    
    volumes:
      certs:
        driver: local
      esdata01:
        driver: local
      esdata02:
        driver: local
      esdata03:
        driver: local
      kibanadata:
        driver: local

#### 在启用并配置安全性的情况下启动群集

1. 修改".env"文件并为"ELASTIC_PASSWORD"和"KIBANA_PASSWORD"变量输入强密码值。

必须使用"ELASTIC_PASSWORD"值与群集进行进一步交互。"KIBANA_PASSWORD"值仅在配置 Kibana 时在内部使用。

2. 创建并启动三节点 Elasticsearch 集群和 Kibana 实例：docker-compose up -d

3. 部署启动后，打开浏览器并导航到 <http://localhost:5601> 以访问 Kibana，您可以在其中加载示例数据并与集群进行交互。

#### 停止并删除部署

要停止集群，请运行"docker-compose down"。Docker 卷中的数据将在使用"docker-compose up"重新启动集群时保留和加载。

    
    
    docker-compose down

要在停止群集时**删除**网络、容器和卷，请指定"-v"选项：

    
    
    docker-compose down -v

#### 后续步骤

您现在已经设置了一个测试Elasticsearch环境。在开始使用 Elasticsearch 进行认真开发或投入生产之前，请查看在 Docker 正式生产环境中运行 Elasticsearch 时要应用的要求和建议。

### 在生产中使用 Docker 映像

在生产环境中在 Docker 中运行 Elasticsearch 时，以下要求和建议适用。

#### 将"vm.max_map_count"设置为至少"262144"

"vm.max_map_count"内核设置必须至少设置为"262144"才能用于生产用途。

如何设置"vm.max_map_count"取决于您的平台。

#####Linux

要查看"vm.max_map_count"设置的当前值，请运行：

    
    
    grep vm.max_map_count /etc/sysctl.conf
    vm.max_map_count=262144

要在实时系统上应用该设置，请运行：

    
    
    sysctl -w vm.max_map_count=262144

要永久更改"vm.max_map_count"设置的值，请更新"/etc/sysctl.conf"中的值。

##### macOS with Docker for Mac

必须在 xhyve 虚拟机中设置"vm.max_map_count"设置：

1. 从命令行运行：screen ~/Library/Containers/com.docker.docker/Data/vms/0/tty

2. 按回车键并使用"sysctl"配置"vm.max_map_count"：sysctl -w vm.max_map_count=262144

3. 要退出"屏幕"会话，请键入"Ctrl a d"。

##### Windows 和 macOS with DockerDesktop

"vm.max_map_count"设置必须通过docker-machine设置：

    
    
    docker-machine ssh
    sudo sysctl -w vm.max_map_count=262144

##### Windows with Docker Desktop WSL 2后端

必须在"docker-desktop"WSL实例中设置"vm.max_map_count"设置，然后ElasticSearch容器才能正确启动。有几种方法可以执行此操作，具体取决于你的 Windows 版本和 WSL 版本。

如果你使用的是 Windows 10 版本 22H2 之前的版本，或者如果你使用的是内置版本的 WSL，则必须在每次重新启动 Docker 时手动设置它，然后再启动 ElasticSearch 容器，或者(如果你不希望在每次重新启动时这样做)必须全局设置每个 WSL2 实例以更改"vm.max_map_count"。这是因为这些版本的 WSL 无法正确处理 /etc/sysctl.conf 文件。

若要在每次重新启动时手动设置它，必须在每次重新启动 Docker 时在命令提示符或 PowerShell 窗口中运行以下命令：

    
    
    wsl -d docker-desktop -u root
    sysctl -w vm.max_map_count=262144

如果您使用的是这些版本的 WSL，并且不希望每次重新启动 Docker 时都必须运行这些命令，则可以通过修改 %USERPROFILE%\\.wslconfig 来全局更改每个 WSL 分发，如下所示：

    
    
    [wsl2]
    kernelCommandLine = "sysctl.vm.max_map_count=262144"

这将导致所有 WSL2 VM 在启动时分配该设置。

如果您使用的是 Windows 11 或 Windows 10 版本 22H2，并且安装了 Microsoft Store 版本的 WSL，则可以在"docker-desktop"WSL 发行版中修改 /etc/sysctl.conf，也许使用如下命令：

    
    
    wsl -d docker-desktop -u root
    vi /etc/sysctl.conf

并附加一行，内容如下：

    
    
    vm.max_map_count = 262144

#### 配置文件必须可由"弹性搜索"用户读取

默认情况下，Elasticsearch 以用户 'elasticsearch' 的身份在容器内运行，使用 uid：gid '1000：0'。

一个例外是Openshift，它使用任意分配的用户ID运行容器.Openshift呈现gid设置为"0"的持久卷，无需任何调整即可工作。

如果要绑定挂载本地目录或文件，则"elasticsearch"用户必须可读取该目录或文件。此外，该用户必须具有对配置、数据和日志目录的写访问权限(Elasticsearch 需要对"config"目录的写访问权限，以便它可以生成密钥库)。一个好的策略是授予组对本地目录的 gid'0' 的访问权限。

例如，要准备一个本地目录以通过绑定挂载存储数据：

    
    
    mkdir esdatadir
    chmod g+rwx esdatadir
    chgrp 0 esdatadir

您还可以使用自定义 UID 和 GID 运行 Elasticsearch 容器。您必须确保文件权限不会阻止 Elasticsearch 执行。您可以使用以下两个选项之一：

* 绑定挂载"配置"、"数据"和"日志"目录。如果您打算安装插件并且不想创建自定义 Docker 镜像，则还必须绑定挂载"插件"目录。  * 将"--group-add 0"命令行选项传递给"docker run"。这确保了运行 Elasticsearch 的用户也是容器内"根"(GID 0) 组的成员。

#### 增加 nofile 和 nproc 的 ulimits

nofile 和 nproc 的 ulimit 必须可用于 Elasticsearch 容器。验证 Docker 守护程序的初始化系统将它们设置为可接受的值。

要检查 Docker 守护程序默认值中的 ulimits，请运行：

    
    
    docker run --rm docker.elastic.co/elasticsearch/elasticsearch:{version} /bin/bash -c 'ulimit -Hn && ulimit -Sn && ulimit -Hu && ulimit -Su'

如果需要，请在守护程序中调整它们或按容器覆盖它们。例如，当使用"docker run"时，设置：

    
    
    --ulimit nofile=65535:65535

#### 禁用交换

需要禁用交换以提高性能和节点稳定性。有关执行此操作的方法的信息，请参阅禁用交换。

如果您选择 'bootstrap.memory_lock： true' 方法，您还需要在 DockerDaemon 中定义 'memlock： true' ulimit，或者为容器显式设置，如示例组合文件中所示。使用"docker run"时，您可以指定：

    
    
    -e "bootstrap.memory_lock=true" --ulimit memlock=-1:-1

#### 随机化已发布端口

映像公开 TCP 端口 9200 和 9300。对于生产群集，建议使用"--publish-all"随机化已发布的端口，除非为每个主机固定一个容器。

#### 手动设置堆大小

默认情况下，Elasticsearch 会根据节点的角色和节点容器可用的总内存自动调整 JVM 堆的大小。对于大多数生产环境，我们建议使用此默认大小调整。如果需要，您可以通过手动设置 JVM 堆大小来覆盖缺省大小调整。

要在生产环境中手动设置堆大小，请在"/usr/share/elasticsearch/config/jvm.options.d"下绑定挂载一个 JVMoptions 文件，其中包含所需的堆大小设置。

对于测试，您还可以使用"ES_JAVA_OPTS"环境变量手动设置堆大小。例如，要使用 16GB，请使用"docker run"指定"-eES_JAVA_OPTS="-Xms16g -Xmx16g"。"ES_JAVA_OPTS"变量覆盖所有其他 JVM 选项。我们不建议使用"ES_JAVA_OPTS"生产。上面的"docker-compose.yml"文件将堆大小设置为 512MB。

#### 将部署固定到特定映像版本

将您的部署固定到特定版本的 Elasticsearch Docker 镜像。例如"docker.elastic.co/elasticsearch/elasticsearch:8.9.0"。

#### 始终绑定数据卷

您应该使用绑定在"/usr/share/elasticsearch/data"上的卷，原因如下：

1. 容器被杀死，你的 Elasticsearch 节点的数据不会丢失 2.Elasticsearch 对 I/O 敏感，Docker 存储驱动程序不适合快速 I/O 3。它允许使用高级 Docker 卷插件

#### 避免使用 'loop-lvm' 模式

如果您使用的是设备映射器存储驱动程序，请不要使用默认的"loop-lvm"模式。将 docker-engine 配置为使用 direct-lvm。

#### 集中您的日志

请考虑使用其他日志记录驱动程序集中日志。另请注意，默认的 json 文件日志记录驱动程序不适合生产使用。

### 使用 Docker 配置 Elasticsearch

当你在 Docker 中运行时，Elasticsearch 配置文件是从 '/usr/share/elasticsearch/config/ ' 加载的。

要使用自定义配置文件，请将文件绑定到映像中的配置文件上。

您可以使用 Dockerenvironment 变量设置单独的 Elasticsearch 配置参数。示例撰写文件和单节点示例使用此方法。您可以直接使用设置名称作为环境变量名称。如果无法执行此操作，例如，由于业务流程平台禁止环境变量名称中的句点，则可以通过按如下所示转换设置名称来使用替代样式。

1. 将设置名称更改为大写 2.以"ES_SETTING_"为前缀 3.通过复制任何下划线('_')来转义它们 4.将所有句点 ('.') 转换为下划线 ('_')

例如，'-e bootstrap.memory_lock=true' 变为 '-eES_SETTING_BOOTSTRAP_MEMORY__LOCK=true'。

您可以使用文件的内容来设置"ELASTIC_PASSWORD"或"KEYSTORE_PASSWORD"环境变量的值，方法是在环境变量名称后加上"_FILE"。这对于将密码等机密传递给 Elasticsearch 而不直接指定它们很有用。

例如，要从文件设置 Elasticsearch 引导密码，您可以绑定挂载该文件并将"ELASTIC_PASSWORD_FILE"环境变量设置为挂载位置。如果将密码文件挂载到"/run/secrets/bootstrapPassword.txt"，请指定：

    
    
    -e ELASTIC_PASSWORD_FILE=/run/secrets/bootstrapPassword.txt

您可以覆盖映像的默认命令，以将 Elasticsearchconfiguration 参数作为命令行选项传递。例如：

    
    
    docker run <various parameters> bin/elasticsearch -Ecluster.name=mynewclustername

虽然绑定挂载配置文件通常是生产中的首选方法，但您也可以创建包含配置的自定义 Dockerimage。

#### 挂载 Elasticsearch 配置文件

创建自定义配置文件，并将它们绑定挂载到 Docker 映像中的相应文件上。例如，要将"custom_elasticsearch.yml"与"docker run"绑定挂载，请指定：

    
    
    -v full_path_to/custom_elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml

如果绑定挂载自定义的"elasticsearch.yml"文件，请确保它包含"network.host： 0.0.0.0"设置。此设置可确保节点可访问 HTTP 和传输流量，前提是其端口已公开。Dockerimage 的内置 'elasticsearch.yml' 文件默认包含此设置。

容器使用 uid：gid'1000：0'** 以用户"elasticsearch"身份运行 Elasticsearch。绑定挂载的主机目录和文件必须可由此用户访问，并且数据和日志目录必须可由此用户写入。

#### 创建加密的弹性搜索密钥库

默认情况下，Elasticsearch 将为 securesettings 自动生成密钥库文件。此文件经过模糊处理，但未加密。

要使用密码加密您的安全设置并让它们保留在容器外部，请使用"docker run"命令手动创建密钥库。该命令必须：

* 绑定挂载"配置"目录。该命令将在此目录中创建一个"elasticsearch.keystore"文件。为避免错误，请勿直接绑定挂载"elasticsearch.keystore"文件。  * 使用带有"create -p"选项的"弹性搜索密钥库"工具。系统将提示您输入密钥库的密码。

例如：

    
    
    docker run -it --rm \
    -v full_path_to/config:/usr/share/elasticsearch/config \
    docker.elastic.co/elasticsearch/elasticsearch:8.9.0 \
    bin/elasticsearch-keystore create -p

您还可以使用"docker run"命令在密钥库中添加或更新安全设置。系统将提示您输入设置值。如果密钥库已加密，系统还将提示您输入密钥库密码。

    
    
    docker run -it --rm \
    -v full_path_to/config:/usr/share/elasticsearch/config \
    docker.elastic.co/elasticsearch/elasticsearch:8.9.0 \
    bin/elasticsearch-keystore \
    add my.secure.setting \
    my.other.secure.setting

如果您已经创建了密钥库并且不需要更新它，则可以直接绑定挂载"elasticsearch.keystore"文件。您可以使用"KEYSTORE_PASSWORD"环境变量在启动时向容器提供密钥库密码。例如，"docker run"命令可能具有以下选项：

    
    
    -v full_path_to/config/elasticsearch.keystore:/usr/share/elasticsearch/config/elasticsearch.keystore
    -e KEYSTORE_PASSWORD=mypassword

#### 使用自定义 Docker 映像

在某些环境中，准备包含配置的自定义映像可能更有意义。实现此目的的"Dockerfile"可能很简单：

    
    
    FROM docker.elastic.co/elasticsearch/elasticsearch:8.9.0
    COPY --chown=elasticsearch:elasticsearch elasticsearch.yml /usr/share/elasticsearch/config/

然后，可以使用以下命令生成和运行映像：

    
    
    docker build --tag=elasticsearch-custom .
    docker run -ti -v /usr/share/elasticsearch/data elasticsearch-custom

某些插件需要额外的安全权限。您必须通过以下方式明确接受它们：

* 在运行 Docker 镜像时附加"tty"，并在出现提示时允许权限。  * 检查安全权限并通过在插件安装命令中添加"--batch"标志来接受它们(如果适用)。

有关详细信息，请参阅插件管理。

#### 排查 Docker 错误 Elasticsearch

下面介绍了如何解决使用 Docker 运行 Elasticsearch 时的常见错误。

#### elasticsearch.keystore is a directory

    
    
    Exception in thread "main" org.elasticsearch.bootstrap.BootstrapException: java.io.IOException: Is a directory: SimpleFSIndexInput(path="/usr/share/elasticsearch/config/elasticsearch.keystore") Likely root cause: java.io.IOException: Is a directory

与密钥库相关的"docker run"命令试图直接绑定挂载不存在的"elasticsearch.keystore"文件。如果使用"-v"或"--volume"标志挂载不存在的文件，Docker 会改为创建一个同名的目录。

要解决此错误，请执行以下操作：

1. 删除"配置"目录中的"elasticsearch.keystore"目录。  2. 更新"-v"或"--volume"标志以指向"配置"目录路径，而不是密钥库文件的路径。有关示例，请参阅创建加密的 Elasticsearch 密钥库。  3. 重试该命令。

#### elasticsearch.keystore： Device or resourcebusy

    
    
    Exception in thread "main" java.nio.file.FileSystemException: /usr/share/elasticsearch/config/elasticsearch.keystore.tmp -> /usr/share/elasticsearch/config/elasticsearch.keystore: Device or resource busy

"docker run"命令试图更新密钥库，同时直接绑定挂载"elasticsearch.keystore"文件。要更新密钥库，容器需要访问"config"目录中的其他文件，例如"密钥库.tmp"。

要解决此错误，请执行以下操作：

1. 更新"-v"或"--volume"标志以指向"配置"目录路径，而不是密钥库文件的路径。有关示例，请参阅创建加密的 Elasticsearch 密钥库。  2. 重试该命令。

[« Install Elasticsearch with RPM](rpm.md) [Run Elasticsearch locally
»](run-elasticsearch-locally.md)
