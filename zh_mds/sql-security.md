

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md)

[« Mapping concepts across SQL and
Elasticsearch](_mapping_concepts_across_sql_and_elasticsearch.md) [SQL REST
API »](sql-rest.md)

##Security

Elasticsearch SQL与安全性集成，前提是在您的集群上启用了此功能。在这种情况下，Elasticsearch SQL支持传输层的安全性(通过加密消费者和服务器之间的通信)和身份验证(访问层)。

#### SSL/TLS 配置

在加密传输的情况下，需要在Elasticsearch SQL中启用SSL/TLS支持，以便与Elasticsearch正确建立通信。这是通过将"ssl"属性设置为"true"或使用URL中的"https"前缀来完成的。 根据您的 SSL 配置(无论证书是否由 aCA 签名，无论它们是 JVM 级别的全局还是只是一个应用程序的本地)，可能需要设置"密钥库"和/或"信任库"，即存储 _credentials_ 的位置("密钥库"\- 通常存储私钥和证书)以及如何_验证_它们("信任库"\- 通常存储来自第三方的证书，也称为 CA 证书颁发机构)。 通常(再次注意，您的环境可能有很大不同)，如果Elasticsearch SQL的SSL设置尚未在JVM级别完成，那么如果Elasticsearch SQLsecurity需要客户端身份验证(PKI - 公钥基础设施)，则需要设置密钥库，如果启用了SSL，则需要设置"信任库"。

####Authentication

Elasticsearch SQL中的身份验证支持有两种类型：

Username/Password

     Set these through `user` and `password` properties. 
PKI/X.509

     Use X.509 certificates to authenticate Elasticsearch SQL to Elasticsearch. For this, one would need to setup the `keystore` containing the private key and certificate to the appropriate user (configured in Elasticsearch) and the `truststore` with the CA certificate used to sign the SSL/TLS certificates in the Elasticsearch cluster. That is, one should setup the key to authenticate Elasticsearch SQL and also to verify that is the right one. To do so, one should set the `ssl.keystore.location` and `ssl.truststore.location` properties to indicate the `keystore` and `truststore` to use. It is recommended to have these secured through a password in which case `ssl.keystore.pass` and `ssl.truststore.pass` properties are required. 

#### 权限(服务器端)

在服务器上，需要向用户添加一些权限，以便他们可以运行SQL。要运行SQL，用户至少需要"read"和"index：admin/get"权限，而API的某些部分需要"cluster：monitor/main"。

您可以通过创建角色并将该角色分配给用户来添加权限。可以使用 Kibana、API 调用或"roles.yml"配置文件创建角色。使用 Kibana 或角色管理 API 是定义角色的首选方法。如果要定义不需要更改的角色，则基于文件的角色管理非常有用。不能使用角色管理 API 查看或编辑在"roles.yml"中定义的角色。

##### 使用角色管理API添加权限

此示例配置一个角色，该角色可以在 JDBC 中运行 SQL 查询"test"索引：

    
    
    POST /_security/role/cli_or_drivers_minimal
    {
      "cluster": ["cluster:monitor/main"],
      "indices": [
        {
          "names": ["test"],
          "privileges": ["read", "indices:admin/get"]
        }
      ]
    }

##### 向"角色.yml"添加权限

此示例配置一个角色，该角色可以在 JDBC 中运行 SQL，以查询"test"和"bort"索引。将以下内容添加到"roles.yml"：

    
    
    cli_or_drivers_minimal:
      cluster:
        - "cluster:monitor/main"
      indices:
        - names: test
          privileges: [read, "indices:admin/get"]
        - names: bort
          privileges: [read, "indices:admin/get"]

[« Mapping concepts across SQL and
Elasticsearch](_mapping_concepts_across_sql_and_elasticsearch.md) [SQL REST
API »](sql-rest.md)
