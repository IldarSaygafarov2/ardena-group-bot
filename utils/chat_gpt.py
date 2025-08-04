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
    забери значения полей 

    "7 Справочный номер" 
    "18 Транспортное средство при отправлении"
    "Вес брутто"
    "Вес нетто"
    "Количество мест"

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
