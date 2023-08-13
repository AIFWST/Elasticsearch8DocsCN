

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[User authentication](setting-up-
authentication.md)

[« Realms](realms.md) [Security domains »](security-domain.md)

## 领域链

领域存在于_realm chain_之中。它本质上是已配置领域(通常为各种类型的)的优先级列表。领域按升序进行咨询(也就是说，首先咨询具有最低"顺序"值的领域)。您必须确保每个已配置的领域都有不同的"顺序"设置。如果两个或多个领域具有相同的"顺序"，节点将无法启动。

在身份验证过程中，Elastic Stack 安全功能会咨询并尝试对请求进行身份验证，一次对一个领域进行身份验证。一旦其中一个领域成功验证了请求，身份验证就被视为成功。经过身份验证的用户与请求相关联，然后进入授权阶段。如果某个领域无法对请求进行身份验证，则会咨询链中的下一个领域。如果链中的所有领域都无法对请求进行身份验证，则身份验证将被视为不成功，并返回身份验证错误(作为 HTTP 状态代码"401")。

某些系统(例如 Active Directory)在多次连续失败的登录尝试后有一个临时锁定期。如果多个领域中存在相同的用户名，则可能会意外锁定帐户。有关详细信息，请参阅用户经常被锁定在 ActiveDirectory 之外。

默认领域链包含"文件"和"本机"领域。要显式配置领域链，请在 'elasticsearch.yml' 文件中指定该链。如果您的领域链不包含"文件"或"本机"领域，或者没有明确禁用它们，那么"文件"和"本机"领域将按该顺序自动添加到领域链的开头。要选择退出自动行为，您可以使用"顺序"和"启用"设置显式配置"文件"和"本机"领域。

以下代码片段配置了一个领域链，该链启用"文件"领域以及两个 LDAP 领域和一个 Active Directory 领域，但禁用"本机"领域。

    
    
    xpack.security.authc.realms:
      file.file1:
          order: 0
    
      ldap.ldap1:
          order: 1
          enabled: false
          url: 'url_to_ldap1'
          ...
    
      ldap.ldap2:
          order: 2
          url: 'url_to_ldap2'
          ...
    
      active_directory.ad1:
          order: 3
          url: 'url_to_ad'
    
      native.native1:
          enabled: false

如上所示，每个领域都有一个唯一的名称来标识它。每种类型的领域都规定了自己的一组必需和可选设置。也就是说，有些设置是所有领域共有的。

### 将授权委托给另一个领域

某些领域能够在内部执行 _身份验证_，但将角色的查找和分配(即 _authorization_)委托给另一个领域。

例如，您可能希望使用 PKI 领域通过 TLS 客户端证书对用户进行身份验证，然后在 LDAP 领域查找该用户，并使用他们的 LDAP 组分配来确定他们在 Elasticsearch 中的角色。

任何支持检索用户(无需其凭据)的领域都可以用作_authorization realm_(也就是说，其名称可能显示为"authorization_realms"列表中的值之一)。请参阅查找用户而无需身份验证，以进一步说明哪些领域支持此功能。

对于支持此功能的领域，可以通过在身份验证领域上配置"authorization_realms"设置来启用此功能。查看每个领域支持的设置列表，看看它们是否支持"authorization_realms"设置。

如果为某个领域启用了委派授权，那么它将以标准方式(包括相关缓存)对用户进行身份验证，然后在配置的授权域列表中查找该用户。它按照在"authorization_realms"设置中指定的顺序尝试每个领域。用户由主体检索 - 用户在the_authentication_和_authorization realms_中必须具有相同的用户名。如果在任何授权域中都找不到该用户，那么身份验证将失败。

有关更多详细信息，请参阅配置授权委派。

委托授权要求您具有包含自定义身份验证和授权域的订阅。

[« Realms](realms.md) [Security domains »](security-domain.md)
