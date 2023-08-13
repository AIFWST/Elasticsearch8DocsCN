

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[Troubleshooting security](security-
troubleshooting.md)

[« Some settings are not returned via the nodes settings API](security-trb-
settings.md) [Users command fails due to extra arguments »](security-trb-
extraargs.md)

## 授权异常

**Symptoms:**

* 我配置了适当的角色和用户，但仍然收到授权异常。  * 我可以向 LDAP 进行身份验证，但仍然收到授权异常。

**Resolution:**

1. 验证与用户关联的角色名称是否与"roles.yml"文件中定义的角色匹配。您可以使用"弹性搜索用户"工具列出所有用户。任何未知角色都标有"*"。           bin/elasticsearch-users list rdeniro ： admin alpacino ： power_user jacknich ： monitoring，unknown_role* __

__

|

在 'roles.yml' ---|中找不到 'unknown_role--- 有关此命令的更多信息，请参阅 'elasticsearch-users' 命令。

2. 如果要对 LDAP 进行身份验证，则许多配置选项可能会导致此错误。

_group identification_

|

组通过 LDAP 搜索或用户上的"memberOf"属性进行定位。此外，如果关闭子树搜索，它将仅搜索一个级别深度。有关所有选项，请参阅 LDAP 领域设置。这里有很多选项，坚持默认值并不适用于所有情况。   ---|--- _group角色mapping_

|

"role_mapping.yml"文件或此文件的位置可能配置错误。有关详细信息，请参阅安全文件。   _role definition_

|

角色定义可能缺失或无效。   为了帮助跟踪这些可能性，请启用其他日志记录以进一步进行故障排除。可以通过配置以下持久设置来启用调试日志记录：

    
        response = client.cluster.put_settings(
      body: {
        persistent: {
          "logger.org.elasticsearch.xpack.security.authc": 'debug'
        }
      }
    )
    puts response
    
        PUT /_cluster/settings
    {
      "persistent": {
        "logger.org.elasticsearch.xpack.security.authc": "debug"
      }
    }

或者，您可以将以下行添加到"ES_PATH_CONF"配置文件的末尾：

    
        logger.authc.name = org.elasticsearch.xpack.security.authc
    logger.authc.level = DEBUG

有关详细信息，请参阅配置日志记录级别。

成功的身份验证应生成列出组和角色映射的调试语句。

[« Some settings are not returned via the nodes settings API](security-trb-
settings.md) [Users command fails due to extra arguments »](security-trb-
extraargs.md)
