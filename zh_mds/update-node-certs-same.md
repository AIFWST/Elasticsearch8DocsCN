

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[Updating node security
certificates](update-node-certs.md)

[« Updating node security certificates](update-node-certs.md) [Update
security certificates with a different CA »](update-node-certs-different.md)

## 使用相同的 CA 更新证书

此过程假定您有权访问最初生成(或由您的组织持有)并用于对当前正在使用的节点证书进行签名的 CA 证书和密钥。它还假设连接到 HTTP 层上 Elasticsearch 的客户端配置为信任 CA 证书。

如果您有权访问用于签署现有证书的 CA，则只需替换群集中每个节点的证书和密钥。如果您替换每个节点上的现有证书和密钥并使用相同的文件名，Elasticsearch 将使用新的证书和密钥重新加载文件。

您不必重新启动每个节点，但这样做会强制新的 TLS 连接，这是更新证书时的建议做法。因此，以下步骤包括在更新每个证书后重新启动节点。

以下步骤提供了为传输层和 HTTP 层生成新节点证书和密钥的说明。您可能只需要替换其中一个图层的证书，具体取决于您的哪个证书即将过期。

如果您的密钥库受密码保护，密码存储在 Elasticsearch 安全设置中，_and_ 密码需要更改，那么您必须在集群上执行滚动重新启动。您还必须为密钥库使用不同的文件名，以便 Elasticsearch 不会在节点重新启动之前重新加载该文件。

如果您的 CA 已更改，请完成使用其他 CA 更新安全证书中的步骤。

### 为传输层生成新证书

以下示例使用 PKCS#12 文件，但相同的步骤适用于 JKS密钥库。

1. 打开"ES_PATH_CONF/elasticsearch.yml"文件，检查当前正在使用的密钥库的名称和位置。您将对新证书使用相同的名称。

在此示例中，密钥库和信任库指向不同的文件。您的配置可能使用包含证书和 CA 的同一文件。在这种情况下，请包括密钥库和信任库的该文件的路径。

这些说明假定提供的证书由受信任的 CA 签名，并且验证模式设置为"证书"。此设置可确保节点不会尝试执行主机名验证。

    
        xpack.security.transport.ssl.keystore.path: config/elastic-certificates.p12
    xpack.security.transport.ssl.keystore.type: PKCS12
    xpack.security.transport.ssl.truststore.path: config/elastic-stack-ca.p12
    xpack.security.transport.ssl.truststore.type: PKCS12
    xpack.security.transport.ssl.verification_mode: certificate

2. 使用现有 CA，为节点生成密钥库。您必须使用用于签署当前正在使用的证书的 CA。           ./bin/elasticsearch-certutil cert --ca elastic-stack-ca.p12

命令参数

'--<ca_file>ca '

     Name of the CA keystore used to sign your certificates. If you used the `elasticsearch-certutil` tool to generate your existing CA, the keystore name defaults to `elastic-stack-ca.p12`. 

    1. Enter a name for the output file or accept the default of `elastic-certificates.p12`. 
    2. When prompted, enter a password for the node keystore. 

3. 如果您在创建节点密钥库时输入的密码与当前密钥库密码不同，请运行以下命令将密码存储在 Elasticsearch 密钥库中：./bin/elasticsearch-keystore add xpack.security.transport.ssl.keystore.secure_password

4. 在集群中要更新密钥库的当前节点上，开始滚动重启。

停止在指示"执行任何所需更改**"的步骤处，然后继续执行此过程的下一步。

5. 将现有密钥库替换为新的密钥库，确保文件名匹配。例如，'elastic-certificate.p12'。

如果您的密钥库密码正在更改，请使用新文件名保存密钥库，以便 Elasticsearch 在您更新密码之前不会尝试重新加载文件。

6. 如果您需要使用新文件名保存新密钥库，请更新"ES_PATH_CONF/elasticsearch.yml"文件以使用新密钥库的文件名。例如：xpack.security.transport.ssl.keystore.path： config/elastic-certificates.p12 xpack.security.transport.ssl.keystore.type： PKCS12 xpack.security.transport.ssl.truststore.path： config/elastic-stack-ca.p12 xpack.security.transport.ssl.truststore.type： PKCS12

7. 启动更新密钥库的节点。  8. (可选)使用 SSL 证书 API 验证 Elasticsearch 是否加载了新密钥库。           获取/_ssl/证书

9. 如果您只更新传输层(而不是 HTTP 层)的证书，请一次完成一个节点的步骤 4 到步骤 8，直到更新集群中的所有密钥库。然后，您可以完成滚动重新启动的其余步骤。

否则，不要完成滚动重新启动。相反，请继续执行为 HTTP 层生成新证书的步骤。

#### 下一步是什么？

干的好！您已更新传输层的密钥库。如有必要，您还可以更新 HTTP 层的密钥库。如果您没有更新 HTTP 层的密钥库，那么您已经全部设置好了。

### 为 HTTPlayer 生成新证书

其他组件(如 Kibana 或任何 Elastic 语言客户端)在连接到 Elasticsearch 时会验证此证书。

如果您的组织有自己的 CA，则需要生成证书签名请求 (CSR)。CSR 包含您的 CA 用于生成和签署证书的信息。

1. 在集群中安装了 Elasticsearch 的任何节点上，运行 Elasticsearch HTTP 证书工具。           ./bin/elasticsearch-certutil http

此命令生成一个".zip"文件，其中包含要与 Elasticsearch 和 Kibana 一起使用的证书和密钥。每个文件夹都包含一个"自述文件.txt"，说明如何使用这些文件。

    1. When asked if you want to generate a CSR, enter `n`. 
    2. When asked if you want to use an existing CA, enter `y`. 
    3. Enter the absolute path to your CA, such as the path to the `elastic-stack-ca.p12` file. 
    4. Enter the password for your CA. 
    5. Enter an expiration value for your certificate. You can enter the validity period in years, months, or days. For example, enter `1y` for one year. 
    6. When asked if you want to generate one certificate per node, enter `y`.

每个证书都有自己的私钥，并将针对特定的主机名或 IP 地址颁发。

    7. When prompted, enter the name of the first node in your cluster. It's helpful to use the same node name as the value for the `node.name` parameter in the `elasticsearch.yml` file. 
    8. Enter all hostnames used to connect to your first node. These hostnames will be added as DNS names in the Subject Alternative Name (SAN) field in your certificate.

列出用于通过 HTTPS 连接到集群的每个主机名和变体。

    9. Enter the IP addresses that clients can use to connect to your node. 
    10. Repeat these steps for each additional node in your cluster. 

2. 为每个节点生成证书后，在出现提示时输入私钥的密码。  3. 解压缩生成的"弹性搜索-ssl-http.zip"文件。此压缩文件包含两个目录;Elasticsearch 和 Kibana 各一个。在"/elasticsearch"目录中，每个节点都有一个目录，您可以使用自己的"http.p12"文件指定该目录。例如： /node1 |_ README.txt |_ http.p12 |_ sample-elasticsearch.yml /node2 |_ README.txt |_ http.p12 |_ sample-elasticsearch.yml /node3 |_ README.txt |_ http.p12 |_ sample-elasticsearch.yml

4. 如有必要，请重命名"http.p12"文件，以匹配用于 HTTP 客户端通信的现有证书的名称。例如，"node1-http.p12"。  5. 在集群中要更新密钥库的当前节点上，开始滚动重启。

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

[« Updating node security certificates](update-node-certs.md) [Update
security certificates with a different CA »](update-node-certs-different.md)
