import requests,json
class Dingding():
    @classmethod
    def _send_dingding_robot(self,url,content):
        response = requests.post(
    			url=url,
    			headers={'Content-Type':'application/json'},
    			data = content
    		)
        return response.content

    @classmethod
    def _get_send_text_content(self,content):
        return json.dumps({
            'msgtype':'text',
            'text':{
                'content':' 下载地址:  '+content
            }
        })

    @classmethod
    def send_dingding(self,robotUrl,sendRobotContent):
        response = Dingding._send_dingding_robot(
            robotUrl,
            Dingding._get_send_text_content(sendRobotContent)
        )
        print(response)

    @classmethod
    def send_max_dingding(self,files,robot_url,send_robot_url):
        if isinstance(files,list):
            for f in files:
                Dingding.send_dingding(robot_url,send_robot_url+f)
