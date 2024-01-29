from dataclasses import dataclass, field
import datetime

@dataclass
class OptionsData:
    blog_root_path: str
    blog_remote_url: str
    blog_local_url: str
    posts_path: str
    assets_path: str
    templates_path: str
    news_page_path: str
    weather_page_path: str
    auto_publish_at_boot: bool
    need_clan_up: bool
    update_news: bool
    update_weather: bool
    publish_timeout_limit: int
    
@dataclass
class PostData:
    name: str
    categorization: str
    tags: str
    creation_time: datetime
    words_num: int