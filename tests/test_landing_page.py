import allure
import pytest


@allure.id("12869")
@allure.title("Check Discovery Session Link")
def test_discovery_session_link(ultimate_qa_app):
    ultimate_qa_app.landing_page.open()

    expected_link_start = "https://forms.clickup.com/2314027/"

    actual_link = ultimate_qa_app.landing_page.discovery_session_link.get_attribute(
        "href"
    )

    assert (
        expected_link_start in actual_link
    ), f"Expected link to start with {expected_link_start}, but got {actual_link}"


@allure.id("12870")
@allure.title("Check View Courses Button")
def test_view_courses_button(ultimate_qa_app):
    ultimate_qa_app.landing_page.open()

    assert (
        ultimate_qa_app.landing_page.is_view_courses_button_visible()
    ), "View Courses button is not visible"


@allure.id("12871")
@allure.title("Check Top Courses")
@pytest.mark.parametrize(
    "expected_course", ["Web Development", "Python", "UX Design", "HTML & CSS"]
)
def test_top_courses(ultimate_qa_app, expected_course: str):
    """Check if the expected course is in the top courses list"""
    ultimate_qa_app.landing_page.open()

    assert ultimate_qa_app.landing_page.top_courses.is_course_displayed(
        expected_course
    ), f"Expected course {expected_course} is not in the list"


@allure.id("12872")
@allure.title("Check Welcome Message")
def test_welcome_message(ultimate_qa_app):
    ultimate_qa_app.landing_page.open()

    expected_welcome_title = "Learn to Code Websites, Apps & Games"
    expected_welcome_text = (
        "Class aptent taciti sociosqu ad litora torquent per conubia nostra, "
        "per inceptos himenaeos. Sed molestie, velit ut eleifend sollicitudin, "
        "neque orci tempor nulla, id sagittis nisi ante nec arcu."
    )

    actual_welcome_title = (
        ultimate_qa_app.landing_page.welcome_title.text_content.strip()
    )
    actual_welcome_text = ultimate_qa_app.landing_page.welcome_text.text_content.strip()

    soft_assert_msg = ""
    soft_assert_result = True
    if not actual_welcome_title == expected_welcome_title:
        soft_assert_result = False
        soft_assert_msg += (
            f"\nExpected welcome title: \n'{expected_welcome_title}', "
            f"\nbut got \n'{actual_welcome_title}'\n"
        )

    if not actual_welcome_text == expected_welcome_text:
        soft_assert_result = False
        soft_assert_msg += (
            f"\nExpected welcome text: \n'{expected_welcome_text}', "
            f"\nbut got \n'{actual_welcome_text}'\n"
        )

    assert soft_assert_result, soft_assert_msg
