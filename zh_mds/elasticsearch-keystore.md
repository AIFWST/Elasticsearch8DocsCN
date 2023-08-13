

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Command
line tools](commands.md)

[« elasticsearch-croneval](elasticsearch-croneval.md) [elasticsearch-node
»](node-tool.md)

## 弹性搜索密钥库

'elasticsearch-keystore' 命令管理 Elasticsearch keystore 中的安全设置。

###Synopsis

    
    
    bin/elasticsearch-keystore
    ( [add <settings>] [-f] [--stdin]
    | [add-file (<setting> <path>)+]
    | [create] [-p]
    | [has-passwd]
    | [list]
    | [passwd]
    | [remove <setting>]
    | [show [-o <output-file>] <setting>]
    | [upgrade]
    ) [-h, --help] ([-s, --silent] | [-v, --verbose])

###Description

此命令应以将运行 Elasticsearch 的用户身份运行。

目前，所有安全设置都是特定于节点的设置，每个节点上必须具有相同的值。因此，必须在每个节点上运行此命令。

当密钥库受密码保护时，您必须在每次启动 Elasticsearch 时提供密码。

对密钥库的修改不会自动应用于正在运行的 Elasticsearch 节点。对密钥库的任何更改都将在您重新启动 Elasticsearch 时生效。某些安全设置可以在不重新启动的情况下显式重新加载。

只有某些设置设计为从密钥库中读取。但是，没有验证来阻止密钥库中不受支持的设置，它们可能导致 Elasticsearch 无法启动。要查看密钥库中是否支持某个设置，请参阅设置参考。

###Parameters

'添加<settings>'

     Adds settings to the keystore. Multiple setting names can be specified as arguments to the `add` command. By default, you are prompted for the values of the settings. If the keystore is password protected, you are also prompted to enter the password. If a setting already exists in the keystore, you must confirm that you want to overwrite the current value. If the keystore does not exist, you must confirm that you want to create a keystore. To avoid these two confirmation prompts, use the `-f` parameter. 
`add-file (<setting> <path>)+`

     Adds files to the keystore. 
`create`

     Creates the keystore. 
`-f, --force`

     When used with the `add` parameter, the command no longer prompts you before overwriting existing entries in the keystore. Also, if you haven't created a keystore yet, it creates a keystore that is obfuscated but not password protected. 
`-h, --help`

     Returns all of the command parameters. 
`has-passwd`

     Returns a success message if the keystore exists and is password-protected. Otherwise, the command fails with exit code 1 and returns an error message. 
`list`

     Lists the settings in the keystore. If the keystore is password protected, you are prompted to enter the password. 
`-p`

     When used with the `create` parameter, the command prompts you to enter a keystore password. If you don't specify the `-p` flag or if you enter an empty password, the keystore is obfuscated but not password protected. 
`passwd`

     Changes or sets the keystore password. If the keystore is password protected, you are prompted to enter the current password and the new one. You can optionally use an empty string to remove the password. If the keystore is not password protected, you can use this command to set a password. 
`remove <settings>`

     Removes settings from the keystore. Multiple setting names can be specified as arguments to the `remove` command. 
`show <setting>`

     Displays the value of a single setting in the keystore. Pass the `-o` (or `--output`) parameter to write the setting to a file. If writing to the standard output (the terminal) the setting's value is always interpreted as a UTF-8 string. If the setting contains binary data (for example for data that was added via the `add-file` command), always use the `-o` option to write to a file. 
`-s, --silent`

     Shows minimal output. 
`-x, --stdin`

     When used with the `add` parameter, you can pass the settings values through standard input (stdin). Separate multiple values with carriage returns or newlines. See [Add settings to the keystore](elasticsearch-keystore.html#add-string-to-keystore "Add settings to the keystore"). 
`upgrade`

     Upgrades the internal format of the keystore. 
`-v, --verbose`

     Shows verbose output. 

###Examples

#### 创建密钥库

要创建"elasticsearch.keystore"，请使用"create"命令：

    
    
    bin/elasticsearch-keystore create -p

系统将提示您输入密钥库密码。受密码保护的"elasticsearch.keystore"文件与"elasticsearch.yml"文件一起创建。

#### 更改密钥库的密码

要更改"elasticsearch.keystore"的密码，请使用"passwd"命令：

    
    
    bin/elasticsearch-keystore passwd

如果 Elasticsearch 密钥库受密码保护，系统会提示您输入当前密码，然后输入新密码。如果没有密码保护，系统会提示您设置密码。

#### 列出密钥库中的设置

要列出密钥库中的设置，请使用"list"命令。

    
    
    bin/elasticsearch-keystore list

如果 Elasticsearch 密钥库受密码保护，系统会提示您输入密码。

#### 将设置添加到密钥库

敏感的字符串设置，如云插件的身份验证凭据，可以使用"add"命令添加：

    
    
    bin/elasticsearch-keystore add the.setting.name.to.set

系统将提示您输入设置的值。如果 Elasticsearchkeystore 受密码保护，系统还会提示您输入密码。

您还可以使用"add"命令添加多个设置：

    
    
    bin/elasticsearch-keystore add \
      the.setting.name.to.set \
      the.other.setting.name.to.set

系统将提示您输入设置的值。如果 Elasticsearchkeystore 受密码保护，系统还会提示您输入密码。

要通过标准输入 (stdin) 传递设置值，请使用 '--stdin'flag：

    
    
    cat /file/containing/setting/value | bin/elasticsearch-keystore add --stdin the.setting.name.to.set

多个设置的值必须用回车符或换行符分隔。

#### 将文件添加到密钥库

您可以使用"add-file"命令添加敏感文件，例如云插件的身份验证密钥文件。设置和文件路径成对指定，由"设置路径"组成。该设置的值将是将文件添加到密钥库时文件路径的二进制内容。

    
    
    bin/elasticsearch-keystore add-file the.setting.name.to.set /path/example-file.json

您可以使用"add-file"命令添加多个文件：

    
    
    bin/elasticsearch-keystore add-file \
      the.setting.name.to.set /path/example-file.json \
      the.other.setting.name.to.set /path/other-example-file.json

如果 Elasticsearch 密钥库受密码保护，系统会提示您输入密码。

#### 显示密钥库中的设置

要在密钥库中显示设置的值，请使用"show"命令：

    
    
    bin/elasticsearch-keystore show the.name.of.the.setting.to.show

如果设置包含二进制数据，则应使用"-o"(或"--output")选项将其写入文件：

    
    
    bin/elasticsearch-keystore show -o my_file binary.setting.name

如果 Elasticsearch 密钥库受密码保护，系统会提示您输入密码。

#### 从密钥库中删除设置

要从密钥库中除去设置，请使用"remove"命令：

    
    
    bin/elasticsearch-keystore remove the.setting.name.to.remove

您还可以使用"删除"命令删除多个设置：

    
    
    bin/elasticsearch-keystore remove \
      the.setting.name.to.remove \
      the.other.setting.name.to.remove

如果 Elasticsearch 密钥库受密码保护，系统会提示您输入密码。

#### 升级密钥库

有时，密钥库的内部格式会更改。从软件包管理器安装 Elasticsearchis 时，磁盘上的密钥库将在软件包升级期间升级到新格式。在其他情况下，Elasticsearch在节点启动期间执行升级。这要求 Elasticsearch 对包含密钥库的目录具有写入权限。或者，您可以使用"升级"命令手动执行此类升级：

    
    
    bin/elasticsearch-keystore upgrade

[« elasticsearch-croneval](elasticsearch-croneval.md) [elasticsearch-node
»](node-tool.md)
