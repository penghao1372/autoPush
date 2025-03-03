import requests
import json

headers = {"Content-Type": "application/json"}
def get_access_token(appid: str, appsecret: str) -> str:
    """
    获取微信接口调用凭证（有效期7200秒）
    """
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={appsecret}"
    response = requests.get(url)
    data = response.json()
    if 'access_token' in data:
        return data['access_token']
    else:
        raise Exception(f"获取access_token失败: {data}")
def upload_media(access_token: str, file_path: str) -> str:
    """
    上传图片并获取media_id（有效期3天）
    """
    url = f"https://api.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type=image"
    with open(file_path, 'rb') as file:
        files = {'media': file}
        response = requests.post(url, files=files)
        data = response.json()
        if 'media_id' in data:
            return data['media_id']
        else:
            raise Exception(f"上传素材失败: {data}")
def create_article_data(
    title: str,
    content: str,
    thumb_media_id: str,
    author: str = "默认作者",
    digest: str = ""
) -> dict:
    """
    构造符合微信API要求的文章数据
    """
    return {
        "articles": [
            {
                "article_type": "newspic",
                "title": title,
                "content": content,
                "need_open_comment": 1,
                "only_fans_can_comment": 0,
                "image_info": {
                    "image_list": [
                        {
                            "image_media_id": thumb_media_id
                        }
                    ]
                }

            }

        ]
    }
def publish_article(access_token: str, article_data: dict) -> dict:
    # 新建草稿
    urlCg =f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
    payload = json.dumps(article_data, ensure_ascii=False)
    responseCg = requests.post(urlCg,headers=headers, data=payload.encode('utf-8'))
    resultCg = responseCg.json()
    return resultCg
    # 获取草稿id
    #draft_id = resultCg.get("media_id")
    # # 发布草稿 微信开发api有问题,不支持直接显示在主页中
    # url = f"https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token={access_token}"
    # payload = json.dumps({"media_id": draft_id}, ensure_ascii=False)
    # response = requests.post(url, headers=headers, data=payload.encode('utf-8'))
    # result = response.json()
    # return {"status": "success", "publish_id": result.get("publish_id")}



def upload_permanent_image(access_token, image_path):
    """上传永久图片素材"""
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}&type=image"
    try:
        with open(image_path, 'rb') as file:
            files = {'media': file}
            response = requests.post(url, files=files)
            response.raise_for_status()
            result = response.json()
            if 'media_id' in result:
                return result['media_id']
            else:
                raise Exception(f"上传失败：{result}")
    except FileNotFoundError:
        raise Exception("图片文件不存在")
    except Exception as e:
        raise Exception(f"上传图片异常：{str(e)}")

def main():
    appid = "wx6c9eb677611827ac"
    appsecret = "f2f7e9d20928ca330cdad93c3f2ddb96"
    try:
        # 获取凭证
        access_token = get_access_token(appid, appsecret)
        # 上传封面图片
        media_id = upload_permanent_image(access_token, "C:\\Users\\Administrator\\Pictures\\wallhaven-2yl6px.jpg")
        #print(media_id)
        # 获取素材 可以获取也可以自己上传
        # urlSc = f"https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token={access_token}"
        # payloadSc = json.dumps({"type": "image", "offset": 0, "count": 20}, ensure_ascii=False)
        # responseSc = requests.post(urlSc, headers=headers, data=payloadSc.encode('utf-8'))
        # resultSc = responseSc.json()
        # thumb_media_id =  resultSc.get("item")[0].get("media_id")
        # 构造文章数据
        article_data = create_article_data(
            title="Python自动发布测试3",
            content="<p>本文由Python程序自动发布3</p>",
            thumb_media_id=media_id
        )
        # 发布文章
        result = publish_article(access_token,article_data)
        print(result)
    except Exception as e:
        print(f"流程异常: {str(e)}")


if __name__ == "__main__":
    main()