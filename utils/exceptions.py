class ValueNotInformed(Exception):
    def __init__(self, field: str, *args: object) -> None:
        super().__init__(*args)
        self.field = field
    
    def __str__(self) -> str:
        return f'{self.field} não informado' 


class ValueNotValid(Exception):
    def __init__(self, field: str, *args: object) -> None:
        super().__init__(*args)
        self.field = field
    
    def __str__(self) -> str:
        return f'{self.field} possui valores inválidos' 