from typing import List, Union

import allure


def attach_text_to_allure(text: Union[str, List[str]], file_name: str):
    """Attach text file to the Allure report"""
    allure.attach(
        str(text), name=f"{file_name}.txt", attachment_type=allure.attachment_type.TEXT
    )
