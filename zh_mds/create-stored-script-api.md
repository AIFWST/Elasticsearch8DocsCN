

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Script APIs](script-apis.md)

[« Script APIs](script-apis.md) [Delete stored script API »](delete-stored-
script-api.md)

## 创建或更新存储的脚本API

创建或更新存储的脚本或搜索模板。

    
    
    response = client.put_script(
      id: 'my-stored-script',
      body: {
        script: {
          lang: 'painless',
          source: "Math.log(_score * 2) + params['my_modifier']"
        }
      }
    )
    puts response
    
    
    PUT _scripts/my-stored-script
    {
      "script": {
        "lang": "painless",
        "source": "Math.log(_score * 2) + params['my_modifier']"
      }
    }

###Request

"放_scripts/<script-id>"

"发布_scripts/<script-id>"

"放_scripts/<script-id><context>/"

"发布_scripts/<script-id>/<context>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"管理"集群权限才能使用此 API。

### 路径参数

`<script-id>`

     (Required, string) Identifier for the stored script or search template. Must be unique within the cluster. 
`<context>`

     (Optional, string) Context in which the script or search template should run. To prevent errors, the API immediately compiles the script or template in this context. 

### 查询参数

`context`

    

(可选，字符串)脚本或搜索模板应在其中运行的上下文。为了防止错误，API 会立即在此上下文中编译脚本或模板。

如果同时指定此参数和 '' 请求路径参数<context>，API 将使用请求路径参数。

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

### 请求正文

`script`

    

(必填，对象)包含脚本或搜索模板、其参数及其语言。

"脚本"的属性

`lang`

     (Required, string) [Script language](modules-scripting.html#scripting-available-languages "Available scripting languages"). For search templates, use `mustache`. 
`source`

    

(必需、字符串或对象)对于脚本，包含脚本的字符串。

对于搜索模板，指包含搜索模板的对象。该对象支持与搜索 API 的请求正文相同的参数。还支持胡子变量。请参阅_Search templates_。

`params`

     (Optional, object) Parameters for the script or search template. 

[« Script APIs](script-apis.md) [Delete stored script API »](delete-stored-
script-api.md)
