

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[Troubleshooting security](security-
troubleshooting.md)

[« Setup-passwords command fails due to connection failure](trb-security-
setup.md) [Security limitations »](security-limitations.md)

## 由于重新定位配置文件而导致的失败

**Symptoms:**

* Active Directory 或 LDAP 领域在升级到 Elasticsearch 6.3 或更高版本后可能会停止工作。在 6.4 或更高版本中，您可能会在 Elasticsearch 日志中看到指示配置文件位于已弃用位置的消息。

**Resolution:**

默认情况下，在 6.2 及更早版本中，安全配置文件位于"ES_PATH_CONF/x-pack"目录中，其中"ES_PATH_CONF"是定义配置目录位置的环境变量。

在 6.3 及更高版本中，config 目录不再包含"x-pack"目录。存储在此文件夹中的文件，例如"log4j2.properties"，"role_mapping.yml"，"roles.yml"，"users"和"users_roles"文件，现在直接存在于配置目录中。

如果升级到 6.3 或更高版本，则旧的安全配置文件仍存在于"x-pack"文件夹中。但是，该文件路径已弃用，您应该将文件移出该文件夹。

在 6.3 及更高版本中，"files.role_mapping"等设置默认为"ES_PATH_CONF/role_mapping.yml"。如果不想使用默认位置，则必须相应地更新设置。请参阅安全设置。

[« Setup-passwords command fails due to connection failure](trb-security-
setup.md) [Security limitations »](security-limitations.md)
