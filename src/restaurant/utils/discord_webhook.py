import requests
from django.conf import settings


def send_discord_webhook(user, category_restaurants):
    # Discord Webhook을 통해 유저에게 맛집 추천 메시지를 전송

    webhook_url = settings.DISCORD_WEBHOOK_URL

    # 메시지 내용
    embeds = []
    for category, restaurants in category_restaurants.items():
        fields = [
            {
                "name": f":fork_and_knife: {restaurant.name}",
                "value": f"{restaurant.lot_addr} ({restaurant.rating} 점)\n[지도 보기](https://maps.google.com/?q={restaurant.lat},{restaurant.lon})",
                "inline": False,
            }
            for restaurant in restaurants
        ]

        embed = {
            "author": {
                "name": f"카테고리: {category}",
            },
            "fields": fields,
            "footer": {
                "text": "점심 추천 서비스!",
                "icon_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRN9lF93jsUSQ2J5jX4f4OcOvJf4I37mCdrfg&usqp=CAU",
            },
        }
        embeds.append(embed)

    payload = {
        "username": "점심추천",
        "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRN9lF93jsUSQ2J5jX4f4OcOvJf4I37mCdrfg&usqp=CAU",
        "content": f"{user.account}님을 위한 오늘의 점심 추천 맛집 리스트!",
        "embeds": embeds,
    }

    # 요청 보내기
    response = requests.post(webhook_url, json=payload)
    if response.status_code != 204:
        print(f"웹훅 보내기 실패: {response.status_code}, {response.text}")
