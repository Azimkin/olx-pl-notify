from typing import Iterable


class UrlConfig:
    def __init__(self, url: str, filters: Iterable[str] = ()):
        self.url = url
        self.filters = filters


URL_LIST = {
    "Материнки": UrlConfig(
        "https://www.olx.pl/elektronika/komputery/podzespoly-i-czesci/plyty-glowne/?search%5Bfilter_enum_state%5D%5B0%5D=used&search%5Bfilter_enum_state%5D%5B1%5D=new&search%5Border%5D=created_at%3Adesc",
        ["AM5", "X870"]
    ),
    "Процы": UrlConfig(
        "https://www.olx.pl/elektronika/komputery/podzespoly-i-czesci/procesory/?search%5Border%5D=created_at:desc&search%5Bfilter_enum_state%5D%5B0%5D=new&search%5Bfilter_enum_state%5D%5B1%5D=used",
        ["Ryzen", "AMD"]
    ),
    "SSD's": UrlConfig(
        "https://www.olx.pl/elektronika/komputery/podzespoly-i-czesci/dyski/?search%5Border%5D=created_at:desc&search%5Bfilter_enum_disktype_components_and_parts%5D%5B0%5D=ssd&search%5Bfilter_enum_diskcapacity_components_and_parts%5D%5B0%5D=257gb-512gb&search%5Bfilter_enum_diskcapacity_components_and_parts%5D%5B1%5D=513gb-1000gb&search%5Bfilter_enum_diskcapacity_components_and_parts%5D%5B2%5D=1tb-and-more",
        []
    ),
    'Кулера': UrlConfig(
        "https://www.olx.pl/elektronika/komputery/podzespoly-i-czesci/chlodzenie-do-komputerow/?search%5Bfilter_enum_state%5D%5B0%5D=used&search%5Bfilter_enum_state%5D%5B1%5D=new&search%5Bfilter_enum_coolingtype_components_and_parts%5D%5B0%5D=air",
        ["deepcool", "ak620"]
    )
    #"Оперативки": "https://www.olx.pl/elektronika/komputery/podzespoly-i-czesci/pamieci-ram/?search%5Border%5D=created_at:desc&search%5Bfilter_enum_typeofmemory%5D%5B0%5D=ddr5&search%5Bfilter_enum_totalcapacity%5D%5B0%5D=64gb-and-more",
}


BOT_TOKEN = 'tg-bot-token'
APP_ID = 123123123123
APP_HASH = '12312312312123131312123213'