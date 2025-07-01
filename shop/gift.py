class Gift:
    giftname: str
    cost: int
    desc: str

    def __init__(self, **kwargs):
        self.__dict__ = kwargs

    def can_buy(self, id: int) -> bool:
        return False
    
    def description(self) -> str:
        return self.desc

    def shop_cap(self) -> str:
        return ""

    async def open(self, id: int):
        await ""
