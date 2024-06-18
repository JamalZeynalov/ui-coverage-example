from ui.base.block import BaseBlock


class TopCoursesBlock(BaseBlock):

    def is_course_displayed(self, course_name: str) -> bool:
        return self._is_html_element_displayed(
            f"//div[contains(@class, 'et_pb_module')]//h4[.='{course_name}']"
        )
