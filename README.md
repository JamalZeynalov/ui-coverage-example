# ui-coverage-example

This project is created to generate data for ui-coverage plugin

## Main Parts:

1. Record used locators during testing (in pages and blocks):
   * The codebase: [ui_coverage_helpers.py](utils%2Freporting%2Fui_coverage_helpers.py)
   * [Usage for Pages](https://github.com/JamalZeynalov/ui-coverage-example/blob/99efd6e66744b670a08d8974a7717e8cb2accd4b/ui/base/page.py#L111)
   * [Usage for Blocks](https://github.com/JamalZeynalov/ui-coverage-example/blob/99efd6e66744b670a08d8974a7717e8cb2accd4b/ui/base/block.py#L50)
2. Save all recorded locators after all tests are done. The code is in: [conftest.py](conftest.py)

## How to get `.json` file with locators:

1. Run all tests in the project with Pytest
2. Copy coverage results file: `ui_coverage/used_locators_gw0.json`

### If you run parallely using xdist

1. Run all tests in the project with Pytest and xdist
2. Run the following command to merge all coverage results:
    ```shell
    python merge_ui_coverage_files.py
    ```
3. Copy coverage results file: `used_locators.json`