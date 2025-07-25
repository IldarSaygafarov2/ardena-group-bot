import base64

from openai import OpenAI

from config.loader import app_config

client = OpenAI(api_key=app_config.gpt.api_key)


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def get_response(image_path: str):
    image = encode_image(image_path)
    response = client.responses.create(
        model=app_config.gpt.model,
        input=[  # type: ignore
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": """
    забери значени полей 

    'курс валюты, нужно забрать сумму'
    'тип декларации'
    'Транспортное средство при отправлении'
    'Справочный номер'
    'Вес брутто'
    'Вес нетто'
    'номер грузовой томоженной декларации'

    все эти данные отдай в виде словаря
    и верни только сам словарь, без лишнего текста
    """

                     },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{image}",
                    },
                ],
            }
        ],
    )
    return response
