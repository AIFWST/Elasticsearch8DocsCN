

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[User authentication](setting-up-
authentication.md)

[« Active Directory user authentication](active-directory-realm.md) [LDAP
user authentication »](ldap-realm.md)

## 基于文件的用户身份验证

您可以使用内置的"文件"领域来管理和验证用户。使用"file"领域，用户在群集中每个节点上的本地文件中定义。

作为群集的管理员，您有责任确保在群集中的每个节点上定义相同的用户。Elastic Stacksecurity 功能不提供任何机制来保证这一点。您还应该知道，您无法通过用户 API 在"文件"领域添加或管理用户，也无法在 Kibana 的 **管理 / 安全 / 用户** 页面上添加或管理用户

"文件"领域作为回退或恢复领域非常有用。例如，在集群无响应或安全索引不可用的情况下，或者当您忘记管理用户的密码时。在这种类型的场景中，"文件"领域是一种方便的出路 - 您可以在"文件"领域定义一个新的"管理员"用户，并使用它来登录和重置所有其他用户的凭据。

为了定义用户，安全功能提供了用户命令行工具。使用此工具可以添加和删除用户、分配用户角色以及管理用户密码。

### 配置文件领域

您无需显式配置"文件"领域。默认情况下，"文件"和"本机"领域被添加到领域链中。除非另有配置，否则首先添加"文件"领域，然后添加"本机"领域。

虽然可以定义其他领域的多个实例，但每个节点只能定义 _one_ "file" 领域。

有关"file"领域用户的所有数据都存储在集群中每个节点上的两个文件中："users"和"users_roles"。这两个文件都位于"ES_PATH_CONF"中，并在启动时读取。

"用户"和"users_roles"文件由节点在本地管理，不由群集全局管理。这意味着，对于典型的多节点群集，需要在群集中的每个节点上应用完全相同的更改。

更安全的方法是在其中一个节点上应用更改，并将文件分发或复制到群集中的所有其他节点(手动或使用配置管理系统，如 Puppet 或 Chef)。

1. (可选)将 realm 配置添加到 'xpack.security.authc.realms.file' 命名空间下的 'elasticsearch.yml' 中。至少，您必须设置领域的"order"属性。

例如，以下代码片段显示了一个"文件"领域配置，该配置将"顺序"设置为零，以便首先检查领域：

    
        xpack:
      security:
        authc:
          realms:
            file:
              file1:
                order: 0

您只能在 Elasticsearch 节点上配置一个文件领域。

2. 重新启动弹性搜索。  3. 将用户信息添加到群集中每个节点上的"ES_PATH_CONF/用户"文件中。

"用户"文件存储所有用户及其密码。文件中的每一行都表示一个由用户名和**哈希**和**加盐**密码组成的单个用户条目。

    
        rdeniro:$2a$10$BBJ/ILiyJ1eBTYoRKxkqbuDEdYECplvxnqQ47uiowE7yGqvCEgj9W
    alpacino:$2a$10$cNwHnElYiMYZ/T3K4PvzGeJ1KbpXZp2PfoQD.gfaVdImnHOwIuBKS
    jacknich:{PBKDF2}50000$z1CLJt0MEFjkIK5iEfgvfnA6xq7lF25uasspsTKSo5Q=$XxCVLbaKDimOdyWgLCLJiyoiWpA/XDMe/xtVgn1r5Sg=

为了限制凭据被盗的风险并减少凭据泄露，文件领域根据安全最佳实践存储密码并缓存用户凭据。默认情况下，用户凭据的哈希版本存储在内存中，使用加盐的"sha-256"哈希算法，哈希版本的密码存储在磁盘上，并使用"bcrypt"哈希算法进行加盐和哈希。若要使用不同的哈希算法，请参阅用户缓存和密码哈希算法。

虽然可以使用任何标准文本编辑器直接修改"用户"文件，但我们强烈建议使用 _elasticsearch-users_ 工具来应用所需的更改。

作为群集的管理员，您有责任确保在群集中的每个节点上定义相同的用户。Elasticsearchsecurity特性不提供任何机制来保证这一点。

4. 将角色信息添加到群集中每个节点上的"ES_PATH_CONF/users_roles"文件中。

"users_roles"文件存储与用户关联的角色。例如：

    
        admin:rdeniro
    power_user:alpacino,jacknich
    user:jacknich

每行将一个角色映射到与该角色关联的所有用户的逗号分隔列表。

您可以使用_elasticsearch users_工具更新此文件。必须确保在群集中的每个节点上都进行了相同的更改。

5. (可选)更改检查"用户"和"users_roles"文件的频率。

默认情况下，Elasticsearch 每 5 秒检查一次这些文件是否有更改。您可以通过更改"elasticsearch.yml"文件中的"resource.reload.interval.high"设置来更改此默认行为(因为这是Elasticsearch中的常见设置，因此更改其值可能会影响系统中的其他调度)。

[« Active Directory user authentication](active-directory-realm.md) [LDAP
user authentication »](ldap-realm.md)
