# ui-coverage-example

This project is created to generate data for ui-coverage plugin

## How to use

1. Run all tests in the project with Pytest
2. Copy coverage results file: `ui_coverage/used_locators_gw0.json`

### If you run parallely using xdist

1. Run all tests in the project with Pytest and xdist
2. Run the following command to merge all coverage results:
    ```shell
    python merge_ui_coverage_files.py
    ```
3. Copy coverage results file: `used_locators.json`