import scrapy
from scrapy.http import HtmlResponse
from grustnogram_api_parsing.items import GrustnogramApiParsingItem


class GrustnogramSpider(scrapy.Spider):
    name = "grustnogram"
    allowed_domains = ["grustnogram.ru"]
    start_urls = ["http://api.grustnogram.ru"]
    login_link = 'https://api.grustnogram.ru/sessions'
    grustnologin = 'sanya222'
    passwd = '12345678987654321'
    parse_user = 'ananishnev'

    def parse(self, response: HtmlResponse):
        yield scrapy.FormRequest(
            self.login_link,
            method='POST',
            callback=self.login,
            formdata={'email': self.grustnologin, 'password': self.passwd}
        )

    def login(self, response: HtmlResponse):
        print(f'******************\n{response.json()}\n******************\n')

        j_body = response.json()
        access_token = j_body['data']['access_token']
        if j_body['data']['status'] == 1:
            yield response.follow(
                f'/users/{self.parse_user}',
                callback=self.user_data_parse,
                cb_kwargs={'nickname': self.parse_user, 'access_token': access_token}
            )

    def user_data_parse(self, response: HtmlResponse, nickname, access_token):
        user_id = response.json()['data']['id']
        url_followers = f'https://api.grustnogram.ru/followers/{user_id}'
        url_follow = f'https://api.grustnogram.ru/follow/{user_id}'
        print(f'&&&&&&&&&&&&&&&&\n{response.json()["data"]}\n&&&&&&&&&&&&&&&&\n')

        yield scrapy.FormRequest(
            url_follow,
            method='GET',
            callback=self.get_user_follows,
            headers={'Access-Token': access_token}
        )
        yield scrapy.FormRequest(
            url_followers,
            method='GET',
            callback=self.get_user_followers,
            headers={'Access-Token': access_token}
        )

    def get_user_followers(self, response: HtmlResponse):
        j_body = response.json()['data']
        for user in j_body:
            user_id = user.get('id')
            nickname = user.get('nickname')
            name = user.get('name')
            avatar = user.get('avatar')
            tag = 'Follower'
            yield GrustnogramApiParsingItem(
                id=user_id,
                nickname=nickname,
                name=name,
                avatar=avatar,
                tag=tag
            )

    def get_user_follows(self, response: HtmlResponse):
        j_body = response.json()['data']
        for user in j_body:
            user_id = user.get('id')
            nickname = user.get('nickname')
            name = user.get('name')
            avatar = user.get('avatar')
            tag = 'is Followed'
            yield GrustnogramApiParsingItem(
                id=user_id,
                nickname=nickname,
                name=name,
                avatar=avatar,
                tag=tag
            )
