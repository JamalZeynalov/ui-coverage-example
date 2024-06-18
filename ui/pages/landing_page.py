from ui.base.page import BasePage
from ui.blocks.top_courses import TopCoursesBlock


class LandingPage(BasePage):
    @property
    def path(self) -> str:
        return "/fake-landing-page"

    @property
    def discovery_session_link(self):
        return self._find_html_element(
            "//div[@class='et_pb_menu__menu']//a[.='I want a free DISCOVERY SESSION']"
        )

    @property
    def top_courses(self) -> TopCoursesBlock:
        return self._find_html_element(
            "//div[@class='et_pb_row']/div[contains(@class, 'et-last-child')]",
            element_class=TopCoursesBlock,
        )

    def is_view_courses_button_visible(self):
        return self._is_html_element_displayed("//a[.='View Courses']")

    @property
    def welcome_title(self):
        return self._find_html_element(
            "//div[contains(@class, 'et_pb_row_0')]//div[@class='et_pb_text_inner']/h1"
        )

    @property
    def welcome_text(self):
        return self._find_html_element(
            "(//div[contains(@class, 'et_pb_row_0')]//div[@class='et_pb_text_inner'])[2]"
        )
