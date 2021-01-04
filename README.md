# Slack client CLI

## Description
Image provides a portable version of Slack CLI which allows to send messages to Slack by choosing custom channel, 
app token, message type, etc.  

Circle CI config is used for automatic build & pushing Docker image to repository.

## Parameters
| Name | Description | Type | Default | Required |
|------|-------------|:----:|:-------:|:--------:|
| channel | Slack channel name | string | - | yes |
| message_type | Slack message type | string | - | yes |
| token | Slack app token (xoxb-your-token) | string | - | no |
| message | Slack message. Required if `json_payload` argument was not specified | string | - | no |
| json_payload | Slack message in json payload. Required if `message` argument was not specified | string | - | no |
| color | Slack attachments message color | string | 36A64F | no |
| header | Slack attachments message header | string | - | no |
| footer | Slack attachments message footer | string | - | no |
| debug | Log level | bool | false | no |

## Examples of usage
### Sending blocks type messages
```
slack-cli -c channel --message_type blocks --message "Some message"
```

### Sending attachments type messages
```
slack-cli -c channel --message_type attachments --message "Some message" --color 36A64F --header "Some header" --footer "My footer"
```

### Sending messages using json payload
```
slack-cli -c channel -s blocks -p '[{"type": "section", "text": {"type": "mrkdwn", "text": "Some text 1"}}]'
```


## Build and deploy
Develop and test locally:
```
docker build -t infra-slackclient:tag .
docker run --rm infra-slackclient:tag <script-args>
```

Build and push to docker registry  
OVH:
```
docker build -t infra-slackclient:latest -t 62q52315.gra7.container-registry.ovh.net/public/infra-slackclient:latest
docker push 62q52315.gra7.container-registry.ovh.net/public/infra-slackclient:latest
```

Quay.io:

```
docker build -t infra-slackclient:latest -t quay.io/tictrac/infra-slackclient:latest
docker push quay.io/tictrac/infra-slackclient:latest
```
