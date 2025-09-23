from graphql import GraphQLError

def validate_and_convert_id(id_as_str: str, field_name: str = "id") -> int:
    """
    Args:
        id_str: Строковый ID для конвертации
        field_name: Название поля для сообщений об ошибках. По умолчанию 'id'

    Returns:
        Целочисленный ID
        
    Raises:
        GraphQLError: Если ID невалидный
    """

    if not id_as_str or not id_as_str.strip():
        raise GraphQLError(
            f"{field_name} не может быть пустым",
            extensions={"code": "MISSING_ID", "field": field_name}
        )
    
    try:
        return int(id_as_str)
    except ValueError:
        raise GraphQLError(
            f"Неверное поле {field_name} значение: '{id_as_str}' должно быть целым числом",
            extensions={
                "code": "INVALID_ID_FORMAT",
                "field": field_name,
                "value": id_as_str
            }
        )