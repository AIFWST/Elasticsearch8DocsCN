

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Get roles API](security-api-get-role.md) [Get service account credentials
API »](security-api-get-service-credentials.md)

## 获取服务账号接口

检索有关服务帐户的信息。

目前，只有"弹性/队列服务器"服务帐户可用。

###Request

"获取/_security/服务"

'获取/_security/服务/<namespace>'

'获取/_security/服务/<namespace>/<service>'

###Prerequisites

* 要使用此 API，您必须至少具有"manage_service_account"群集权限。

###Description

此 API 返回与提供的路径参数匹配的服务帐户列表。

### 路径参数

`namespace`

     (Optional, string) Name of the namespace. Omit this parameter to retrieve information about all service accounts. If you omit this parameter, you must also omit the `service` parameter. 
`service`

     (Optional, string) Name of the service name. Omit this parameter to retrieve information about all service accounts that belong to the specified `namespace`. 

### 响应正文

成功的调用会返回服务帐户的 JSON 对象。如果未找到服务帐户，则 API 返回空对象。

###Examples

对于以下请求，检索"弹性/队列服务器"服务帐户的服务帐户：

    
    
    GET /_security/service/elastic/fleet-server
    
    
    {
      "elastic/fleet-server": {
        "role_descriptor": {
          "cluster": [
            "monitor",
            "manage_own_api_key"
          ],
          "indices": [
            {
              "names": [
                "logs-*",
                "metrics-*",
                "traces-*",
                ".logs-endpoint.diagnostic.collection-*",
                ".logs-endpoint.action.responses-*"
              ],
              "privileges": [
                "write",
                "create_index",
                "auto_configure"
              ],
              "allow_restricted_indices": false
            },
            {
              "names": [
                "profiling-*"
              ],
              "privileges": [
                "read",
                "write",
                "auto_configure"
              ],
              "allow_restricted_indices": false
            },
            {
              "names" : [
                "traces-apm.sampled-*"
              ],
              "privileges" : [
                "read",
                "monitor",
                "maintenance"
              ],
              "allow_restricted_indices": false
            },
            {
              "names": [
                ".fleet-secrets*"
              ],
              "privileges": [
                "read",
              ],
              "allow_restricted_indices": true
            },
            {
              "names": [
                ".fleet-*"
              ],
              "privileges": [
                "read",
                "write",
                "monitor",
                "create_index",
                "auto_configure",
                "maintenance"
              ],
              "allow_restricted_indices": true
            },
            {
              "names": [
                "synthetics-*"
              ],
              "privileges": [
                "read",
                "write",
                "create_index",
                "auto_configure"
              ],
              "allow_restricted_indices": false
            }
          ],
          "applications": [
            {
              "application" : "kibana-*",
              "privileges" : [
                "reserved_fleet-setup"
              ],
              "resources" : [
                "*"
              ]
            }
          ],
          "run_as": [],
          "metadata": {},
          "transient_metadata": {
            "enabled": true
          }
        }
      }
    }

省略"命名空间"和"服务"以检索所有服务帐户：

    
    
    GET /_security/service

[« Get roles API](security-api-get-role.md) [Get service account credentials
API »](security-api-get-service-credentials.md)
