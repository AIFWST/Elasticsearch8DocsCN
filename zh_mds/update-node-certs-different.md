

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[Updating node security
certificates](update-node-certs.md)

[« Update certificates with the same CA](update-node-certs-same.md) [User
authentication »](setting-up-authentication.md)

## 使用不同的 CA 更新安全证书

如果您必须信任组织中的新 CA，或者需要自己生成新 CA，请使用此新 CA 对新节点证书进行签名，并指示节点信任新 CA。

### 为传输层生成新证书

创建新的 CA 证书，或获取组织的 CA 证书，并将其添加到现有的 CA 信任库。更新完所有节点的证书后，您可以从信任库中删除旧的 CA 证书(但不能在此之前！

以下示例使用 PKCS#12 文件，但相同的步骤适用于 JKS密钥库。

1. 打开"ES_PATH_CONF/elasticsearch.yml"文件，检查当前正在使用的密钥库的名称和位置。您将对新密钥库使用相同的名称。

在此示例中，密钥库和信任库使用不同的文件。您的配置可以对密钥库和信任库使用相同的文件。

这些说明假定提供的证书由受信任的 CA 签名，并且验证模式设置为"证书"。此设置可确保节点不会尝试执行主机名验证。

    
        xpack.security.transport.ssl.keystore.path: config/elastic-certificates.p12
    xpack.security.transport.ssl.keystore.type: PKCS12
    xpack.security.transport.ssl.truststore.path: config/elastic-stack-ca.p12
    xpack.security.transport.ssl.truststore.type: PKCS12
    xpack.security.transport.ssl.verification_mode: certificate

2. 在集群中的 **any** 节点上，生成新的 CA 证书。您只需完成此步骤一次。如果您使用的是组织的 CA 证书，请跳过此步骤。           ./bin/elasticsearch-certutil ca --pem

命令参数

`--pem`

     Generates a directory containing a CA certificate and key in PEM format instead of PKCS#12. 

    1. Enter a name for the compressed output file that will contain your certificate and key, or accept the default name of `elastic-stack-ca.zip`. 
    2. Unzip the output file. The resulting directory contains a CA certificate (`ca.crt`) and a private key (`ca.key`).

将这些文件保存在安全的位置，因为它们包含您的CA的私钥。

3. 在集群中的每个节点上，将新的"ca.crt"证书导入现有 CA 信任库。此步骤可确保您的集群信任新的 CA 证书。此示例使用 Java 'keytool' 实用程序将证书导入 'elastic-stack-ca.p12' CA 信任库。           keytool -importcert -trustcacerts -noprompt -keystore elastic-stack-ca.p12 \ -storepass -<password>alias new-ca -file ca.crt

命令参数

`-keystore`

     Name of the truststore that you are importing the new CA certificate into. 
`-storepass`

     Password for the CA truststore. 
`-alias`

     Name that you want to assign to the new CA certificate entry in the keystore. 
`-file`

     Name of the new CA certificate to import. 

4. 检查新的 CA 证书是否已添加到您的信任库。           keytool -keystore config/elastic-stack-ca.p12 -list

出现提示时，输入 CA 信任库的密码。

输出应同时包含现有 CA 证书和新证书。如果您之前使用"elasticsearch-certutil"工具来生成密钥库，则旧CA的别名默认为"ca"，条目类型为"PrivateKeyEntry"。

#### 为群集中的每个节点生成新证书

现在您的 CA 信任库已更新，请使用新的 CA 证书为您的节点签署证书。

如果您的组织有自己的 CA，则需要生成证书签名请求 (CSR)。CSR 包含您的 CA 用于生成和签署安全证书的信息。

1. 使用新的 CA 证书和密钥，为您的节点创建新证书。           ./bin/elasticsearch-certutil cert --ca-cert ca/ca.crt --ca-key ca/ca.key

命令参数

`--ca-cert`

     Specifies the path to your new CA certificate (`ca.crt`) in PEM format. You must also specify the `--ca-key` parameter. 
`--ca-key`

     Specifies the path to the private key (`ca.key`) for your CA certificate. You must also specify the `--ca-cert` parameter. 

    1. Enter a name for the output file or accept the default of `elastic-certificates.p12`. 
    2. When prompted, enter a password for your node certificate. 

2. 在集群中要更新密钥库的当前节点上，开始滚动重启。

停止在指示"执行任何所需更改**"的步骤处，然后继续执行此过程的下一步。

3. 将现有密钥库替换为新的密钥库，确保文件名匹配。例如，'elastic-certificate.p12'。

如果您的密钥库密码正在更改，请使用新文件名保存密钥库，以便 Elasticsearch 在您更新密码之前不会尝试重新加载文件。

4. 如果您需要使用新文件名保存新密钥库，请更新"ES_PATH_CONF/elasticsearch.yml"文件以使用新密钥库的文件名。例如：xpack.security.transport.ssl.keystore.path： config/elastic-certificates.p12 xpack.security.transport.ssl.keystore.type： PKCS12 xpack.security.transport.ssl.truststore.path： config/elastic-stack-ca.p12 xpack.security.transport.ssl.truststore.type： PKCS12

5. 启动更新密钥库的节点。  6. (可选)使用 SSL 证书 API 验证 Elasticsearch 是否加载了新密钥库。           获取/_ssl/证书

7. 如果您只更新传输层(而不是 HTTP 层)的证书，请一次完成一个节点的步骤 2 到步骤 6，直到更新集群中的所有密钥库。然后，您可以完成滚动重新启动的其余步骤。

否则，不要完成滚动重新启动。相反，请继续执行为 HTTP 层生成新证书的步骤。

8. (可选)替换集群中每个节点上的密钥库后，列出信任库中的证书，然后除去旧的 CA 证书。

如果您之前使用"elasticsearch-certutil"工具生成密钥库，则旧CA的别名默认为"ca"，条目类型为"PrivateKeyEntry"。

    
        keytool -delete -noprompt -alias ca  -keystore config/elastic-stack-ca.p12 \
    -storepass <password>

命令参数

`-alias`

     Name of the keystore alias for the old CA certificate that you want to remove from your truststore. 

#### 下一步是什么？

干的好！您已更新传输层的密钥库。如有必要，您还可以更新 HTTP 层的密钥库。如果您没有更新 HTTPlayer 的密钥库，那么您已经全部设置好了。

### 为 HTTPlayer 生成新证书

您可以使用新的 CA 证书和私钥为 HTTP 层生成证书。其他组件(如 Kibana 或任何 Elasticlanguage 客户端)在连接到 Elasticsearch 时会验证此证书。

如果您的组织有自己的 CA，则需要生成证书签名请求 (CSR)。CSR 包含您的 CA 用于生成和签署安全证书的信息，而不是使用"弹性搜索-证书util"工具生成的自签名证书。

**更新客户端以信任新的 CA**

在为 HTTP 层生成(但在使用)新证书之后，您需要转到连接到 Elasticsearch 的所有客户端(例如 Beats、Logstash 和任何语言客户端)，并将它们配置为也信任您生成的 newCA ('ca.crt')。

此过程因每个客户端而异，因此请参阅客户端的文档以获取信任证书。在此过程中，您将在生成必要的证书后更新 Kibana 和 Elasticsearch 之间的 HTTP 加密。

1. 在集群中安装了 Elasticsearch 的任何节点上，运行 Elasticsearch HTTP 证书工具。           ./bin/elasticsearch-certutil http

此命令生成一个".zip"文件，其中包含要与 Elasticsearch 和 Kibana 一起使用的证书和密钥。每个文件夹都包含一个"自述文件.txt"，说明如何使用这些文件。

    1. When asked if you want to generate a CSR, enter `n`. 
    2. When asked if you want to use an existing CA, enter `y`. 
    3. Enter the absolute path to your **new** CA certificate, such as the path to the `ca.crt` file. 
    4. Enter the absolute path to your new CA certificate private key, such as the path to the `ca.key` file. 
    5. Enter an expiration value for your certificate. You can enter the validity period in years, months, or days. For example, enter `1y` for one year. 
    6. When asked if you want to generate one certificate per node, enter `y`.

每个证书都有自己的私钥，并将针对特定的主机名或 IP 地址颁发。

    7. When prompted, enter the name of the first node in your cluster. Use the same node name as the value for the `node.name` parameter in the `elasticsearch.yml` file. 
    8. Enter all hostnames used to connect to your first node. These hostnames will be added as DNS names in the Subject Alternative Name (SAN) field in your certificate.

列出用于通过 HTTPS 连接到集群的每个主机名和变体。

    9. Enter the IP addresses that clients can use to connect to your node. 
    10. Repeat these steps for each additional node in your cluster. 

2. 为每个节点生成证书后，在出现提示时输入密钥库的密码。  3. 解压缩生成的"弹性搜索-ssl-http.zip"文件。这个压缩文件包含一个用于Elasticsearch和Kibana的目录。在"/elasticsearch"目录中，每个节点都有一个目录，您可以使用自己的"http.p12"文件指定该目录。例如： /node1 |_ README.txt |_ http.p12 |_ sample-elasticsearch.yml /node2 |_ README.txt |_ http.p12 |_ sample-elasticsearch.yml /node3 |_ README.txt |_ http.p12 |_ sample-elasticsearch.yml

4. 如有必要，重命名每个"http.p12"文件，以匹配用于 HTTP 客户端通信的现有证书的名称。例如，"node1-http.p12"。  5. 在集群中要更新密钥库的当前节点上，开始滚动重启。

停止在指示"执行任何所需更改**"的步骤处，然后继续执行此过程的下一步。

6. 将现有密钥库替换为新的密钥库，确保文件名匹配。例如，"node1-http.p12"。

如果您的密钥库密码正在更改，请使用新文件名保存密钥库，以便 Elasticsearch 在您更新密码之前不会尝试重新加载文件。

7. 如果您需要使用新文件名保存新密钥库，请更新"ES_PATH_CONF/elasticsearch.yml"文件以使用新密钥库的文件名。例如：xpack.security.http.ssl.enabled： true xpack.security.http.ssl.keystore.path： node1-http.p12

8. 如果您的密钥库密码正在更改，请将私钥的密码添加到 Elasticsearch 的安全设置中。           ./bin/elasticsearch-keystore add xpack.security.http.ssl.keystore.secure_password

9. 启动更新密钥库的节点。

使用 cat 节点 API 确认节点已加入群集：

    
        response = client.cat.nodes
    puts response
    
        GET _cat/nodes

10. (可选)使用 SSL 证书 API 验证 Elasticsearch 是否加载了新密钥库。           获取/_ssl/证书

11. 一次一个节点，完成步骤 5 到步骤 10，直到更新集群中的所有密钥库。  12. 完成滚动重启的其余步骤，从**重新启用分片分配**的步骤开始。

#### 下一步是什么？

干的好！您已更新 HTTP 层的密钥库。您现在可以在 Kibana 和 Elasticsearch 之间更新加密。

### 更新 Kibana 和 Elasticsearch 之间的加密

当你使用"http"选项运行"elasticsearch-certutil"工具时，它创建了一个包含"elasticsearch-ca.pem"文件的"/kibana"目录。您可以使用此文件将 Kibana 配置为信任 HTTPlayer 的 Elasticsearch CA。

1. 将 'elasticsearch-ca.pem' 文件复制到 Kibana 配置目录，如"KBN_PATH_CONF"路径所定义。

"KBN_PATH_CONF"包含 Kibana 配置文件的路径。如果您使用归档发行版("zip"或"tar.gz")安装了 Kibana，则路径默认为"KBN_HOME/config"。如果您使用的是软件包发行版(Debian 或 RPM)，则路径默认为 '/etc/kibana'。

2. 如果您修改了"elasticsearch-ca.pem"文件的文件名，请编辑"kibana.yml"并更新配置以指定 HTTP 层的安全证书的位置。           elasticsearch.ssl.certificateAuthority： KBN_PATH_CONF/elasticsearch-ca.pem

3. 重新启动 Kibana。

[« Update certificates with the same CA](update-node-certs-same.md) [User
authentication »](setting-up-authentication.md)
