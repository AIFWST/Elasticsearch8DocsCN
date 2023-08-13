

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md)

[« Clear cache API](searchable-snapshots-api-clear-cache.md) [Authenticate
API »](security-api-authenticate.md)

## 安全接口

要使用安全 API，您必须在"elasticsearch.yml"文件中将"xpack.security.enabled"设置为"true"。

使用以下 API 执行安全活动。

* 身份验证 * 清除缓存 * 委托 PKI 身份验证 * 具有权限 * SSL 证书 * 获取内置权限 * 获取用户权限

### 应用程序权限

使用以下 API 添加、更新、检索和删除应用程序权限：

* 创建或更新权限 * 清除权限缓存 * 删除权限 * 获取权限

### 角色映射

使用以下 API 添加、删除、更新和检索角色映射：

* 创建或更新角色映射 * 删除角色映射 * 获取角色映射

###Roles

使用以下 API 在本机域中添加、删除、更新和检索角色：

* 创建或更新角色 * 清除角色缓存 * 删除角色 * 获取角色

###Tokens

使用以下 API 创建持有者令牌并使其失效以进行访问，而无需基本身份验证：

* 获取令牌 * 使令牌无效

### APIKeys

使用以下 API 创建、检索和失效用于访问的 API 密钥，而无需基本身份验证：

* 创建 API 密钥 * 获取 API 密钥 * 使 API 密钥失效 * 清除 API 密钥缓存 * 授予 API 密钥 * 查询 API 密钥 * 更新 API 密钥 * 批量更新 API 密钥

###Users

使用以下 API 在本机领域添加、删除、更新或检索用户：

* 创建或更新用户 * 更改密码 * 删除用户 * 禁用用户 * 启用用户 * 获取用户

### 服务帐户

使用以下 API 列出服务帐户并管理服务令牌：

* 获取服务帐户 * 创建服务帐户令牌 * 删除服务帐户令牌 * 获取服务帐户凭据

### OpenIDConnect

使用以下 API 在使用 Kibana 以外的自定义 Web 应用程序时，根据 OpenID Connectauthentication 领域对用户进行身份验证

* 准备身份验证请求 * 提交身份验证响应 * 注销经过身份验证的用户

###SAML

使用 Kibana 以外的自定义 Web 应用程序时，使用以下 API 根据 SAML 身份验证域对用户进行身份验证

* 准备身份验证请求 * 提交身份验证响应 * 注销经过身份验证的用户 * 从 IdP 提交注销请求 * 验证来自 IdP 的注销响应 * 生成 SAML 元数据

###Enrollment

使用以下 API 使新节点能够加入启用了安全性的现有集群，或者使 Kibana 实例能够将自身配置为与安全的 Elasticsearch 集群通信。

* 注册新节点 * 注册新的 Kibana 实例

### 用户配置文件

使用以下 API 检索和管理用户配置文件。

* 激活用户配置文件 * 获取用户配置文件 * 更新用户配置文件数据 * 启用用户配置文件 * 禁用用户配置文件 * 建议用户配置文件 * 具有权限用户配置文件

[« Clear cache API](searchable-snapshots-api-clear-cache.md) [Authenticate
API »](security-api-authenticate.md)
