

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[User authentication](setting-up-
authentication.md)

[« Realm chains](realm-chains.md) [Active Directory user authentication
»](active-directory-realm.md)

## 安全域

安全域是一种将多个领域分组到同一域下的方法，以便 Elastic Stack 可以识别单个用户何时使用这些领域进行身份验证。用户可以使用域组中的任何领域进行身份验证，并且无论使用哪个领域进行身份验证，都可以访问同一组资源。

例如，单个用户配置文件与用户相关联，从而允许跨领域共享首选项、通知和其他用户数据。用户可以查看来自异步搜索请求或跨领域的滚动搜索的结果。如果用户具有必要的权限，他们还可以跨领域查看和管理 API 密钥。

### 跨域资源共享

Elasticsearch 中的某些类型的资源由单个用户拥有，例如异步搜索上下文、API 密钥和用户配置文件。当用户创建资源时，Elasticsearch 会捕获用户的用户名和领域信息作为资源元数据的一部分。同样，如果用户更新资源(例如 API 密钥)，Elasticsearch 会自动重新捕获用户的当前领域信息。

当用户稍后尝试访问资源时，Elasticsearch 会将捕获的用户名和领域信息与访问用户的信息进行比较。Elasticsearch 将拒绝访问，除非领域和用户名都匹配。如果 Lasticsearch 检测到来自两个不同领域的用户名正在尝试访问资源，则 Elasticsearch 假定这些用户是不同的，并且不允许在这些用户之间共享资源。

但是，在某些情况下，同一用户可以向多个领域进行身份验证，并且需要跨领域共享同一组资源。例如，LDAP 领域和 aSAML 领域可以由相同的目录服务提供支持。此外，授权委派允许一个领域将授权委托给另一个领域。如果两个领域都使用相同的用户名对用户进行身份验证，则从资源所有权的角度来看，将这些用户视为同一用户是合理的。

安全域通过将域分组到同一域下，使跨领域资源共享成为可能。Elasticsearch 始终强制执行与当前经过身份验证的用户关联的权限，对于安全域来说，这仍然是正确的。当资源共享需要安全域时，它们不会绕过用户授权。例如，用户需要"manage_own_api_key"权限来管理自己的 API 密钥。如果该用户在向一个领域进行身份验证时没有此权限，则在使用另一个领域进行身份验证时，他们将无法管理 API 密钥。

#### 跨领域管理角色

Elasticsearch 提供了多种方法来跨领域一致地应用角色。例如，您可以使用授权委派来确保从多个领域为用户分配相同的角色。您还可以手动配置由同一目录服务支持的多个领域。尽管在使用不同领域进行身份验证时可以为同一用户配置不同的角色，但 _不_ 建议这样做。

### 配置安全域

安全域是一项需要仔细配置的高级功能。配置错误或误用可能会导致意外行为。

必须在群集中的所有节点上一致地配置安全域。配置不一致可能会导致以下问题：

* 重复的用户配置文件 * 根据身份验证节点的配置，资源所有权不同

配置安全域：

1. 将安全域配置添加到"xpack.security.authc.domains"命名空间中的"elasticsearch.yml"：xpack：security：authc：domain：my_domain：realms：[ 'default_native'， 'saml1' ] __

__

|

此配置定义了一个名为"my_domain"的安全域，其中包含名为"default_native"和"saml1"的两个域。   ---|--- 指定的领域必须在 'elasticsearch.yml' 中定义，但不需要启用。

文件领域和本机领域分别自动启用为"default_file"和"default_native"，无需任何显式配置。您可以在域下列出这些领域，即使它们没有在"elasticsearch.yml"中明确定义。

2. 重新启动弹性搜索。

如果域配置无效，Elasticsearch 可能无法启动，例如：

    * The same realm is configured under multiple domains. 
    * Any undefined realm, synthetic realm, or the reserved realm is configured to be under a domain. 

3. 在执行与安全域相关的操作(包括创建和管理用户配置文件、API 密钥和异步搜索等资源)之前，对集群中的所有节点应用相同的配置。

将领域添加到安全域时，在将更改完全应用于所有节点之前，请避免使用新添加的领域进行身份验证。

### 从安全域中删除领域

从安全域中除去域可能会导致意外行为，因此不建议这样做。删除之前创建或更新的资源可以由不同的用户拥有，具体取决于资源类型：

* 用户配置文件归上次激活配置文件的用户所有。对于领域不再与所有者用户位于同一域中的用户，下次调用激活用户配置文件 API 时，将为其创建新的用户配置文件。  * API 密钥归最初创建或上次更新它的用户所有。如果用户(包括 API 密钥的原始创建者)的领域不再与当前 API 密钥所有者的域位于同一域中，则其所有权将丧失。  * 异步搜索上下文等资源归最初创建它们的用户所有。

与其除去领域，不如考虑禁用它们并将其保留为安全域的一部分。在任何情况下，跨领域的资源共享只能在具有相同用户名的用户之间进行。

[« Realm chains](realm-chains.md) [Active Directory user authentication
»](active-directory-realm.md)
