

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Command
line tools](commands.md)

[« elasticsearch-syskeygen](syskeygen.md) [How to »](how-to.md)

## 弹性搜索用户

如果使用基于文件的用户身份验证，则"弹性搜索用户"命令使您能够添加和删除用户、分配用户角色以及管理每个节点的密码。

###Synopsis

    
    
    bin/elasticsearch-users
    ([useradd <username>] [-p <password>] [-r <roles>]) |
    ([list] <username>) |
    ([passwd <username>] [-p <password>]) |
    ([roles <username>] [-a <roles>] [-r <roles>]) |
    ([userdel <username>])

###Description

如果使用内置的"file"内部领域，则会在群集中每个节点上的 localfile 中定义用户。

用户名和角色必须至少为 1 个字符且不超过 1024 个字符。它们可以包含字母数字字符("a-z"、"A-Z"、"0-9")、空格、标点符号和基本拉丁语 (ASCII) 块中的可打印符号)。不允许使用前导或尾随空格。

密码长度必须至少为 6 个字符。

有关详细信息，请参阅基于文件的用户身份验证。

为了确保 Elasticsearch 可以在启动时读取用户和角色信息，请以运行 Elasticsearch 的同一用户身份运行 'elasticsearch-users useradd'。以 root 或其他用户身份运行命令会更新"用户"和"users_roles"文件的权限，并阻止 Elasticsearch 访问它们。

###Parameters

'-a <roles>'

     If used with the `roles` parameter, adds a comma-separated list of roles to a user. 

`list`

     List the users that are registered with the `file` realm on the local node. If you also specify a user name, the command provides information for that user. 
`-p <password>`

    

指定用户的密码。如果未指定此参数，该命令将提示您输入密码。

省略"-p"选项以将明文密码排除在终端会话的命令历史记录之外。

"咔嚓<username>"

     Resets a user's password. You can specify the new password directly with the `-p` parameter. 
`-r <roles>`

    

* 如果与"useradd"参数一起使用，则定义用户的角色。此选项接受要分配给用户的角色名称的逗号分隔列表。  * 如果与"roles"参数一起使用，则会从用户中删除以逗号分隔的角色列表。

`roles`

     Manages the roles of a particular user. You can combine adding and removing roles within the same command to change a user's roles. 

'用户添加 <username>'

     Adds a user to your local node. 
`userdel <username>`

     Deletes a user from your local node. 

###Examples

下面的示例将一个名为"jacknich"的新用户添加到"file"领域。此用户的密码为"theshining"，并且此用户与"网络"和"监视"角色相关联。

    
    
    bin/elasticsearch-users useradd jacknich -p theshining -r network,monitoring

以下示例列出了在本地节点上的"file"域中注册的用户：

    
    
    bin/elasticsearch-users list
    rdeniro        : admin
    alpacino       : power_user
    jacknich       : monitoring,network

用户位于左侧列中，其相应的角色列在右侧列中。

以下示例重置"jacknich"用户的密码：

    
    
    bin/elasticsearch-users passwd jachnich

由于省略了"-p"参数，该命令会提示您在交互模式下输入并确认密码。

以下示例从"jacknich"用户中删除"网络"和"监视"角色，并添加"用户"角色：

    
    
    bin/elasticsearch-users roles jacknich -r network,monitoring -a user

以下示例删除"jacknich"用户：

    
    
    bin/elasticsearch-users userdel jacknich

[« elasticsearch-syskeygen](syskeygen.md) [How to »](how-to.md)
