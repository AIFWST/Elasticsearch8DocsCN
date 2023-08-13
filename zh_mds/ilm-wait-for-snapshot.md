

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Data
management](data-management.md) ›[Index lifecycle actions](ilm-actions.md)

[« Unfollow](ilm-unfollow.md) [Configure a lifecycle policy »](set-up-
lifecycle-policy.md)

## 等待快照

允许的阶段：删除。

等待指定的 SLM 策略执行，然后再删除索引。这可确保已删除索引的快照可用。

###Options

`policy`

     (Required, string) Name of the SLM policy that the delete action should wait for. 

###Example

    
    
    PUT _ilm/policy/my_policy
    {
      "policy": {
        "phases": {
          "delete": {
            "actions": {
              "wait_for_snapshot" : {
                "policy": "slm-policy-name"
              }
            }
          }
        }
      }
    }

[« Unfollow](ilm-unfollow.md) [Configure a lifecycle policy »](set-up-
lifecycle-policy.md)
