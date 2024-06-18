import json
import os
from pathlib import Path

import rootpath


def merge_ui_coverage_json_files(input_dir_path, output_dir_path):
    merged_data = {}
    for filename in os.listdir(input_dir_path):
        if filename.endswith(".json"):
            file_path = os.path.join(input_dir_path, filename)
            with open(file_path, "r") as file:
                data = json.load(file)
                for url, xpaths_dict in data.items():
                    if url in merged_data:
                        # Merge XPath keys and their corresponding lists of dictionaries
                        for xpath, test_cases in xpaths_dict.items():
                            if xpath in merged_data[url]:
                                merged_data[url][xpath].extend(test_cases)
                            else:
                                merged_data[url][xpath] = test_cases
                    else:
                        merged_data[url] = xpaths_dict

    # remove duplicates allure_id
    # pylint: disable=consider-using-dict-items
    for url in merged_data:
        for xpath in merged_data[url]:
            merged_data[url][xpath] = [
                item
                for i, item in enumerate(merged_data[url][xpath])
                if item["allure_id"]
                not in {x["allure_id"] for x in merged_data[url][xpath][:i]}
            ]

    # Write the merged data to a new JSON file
    output_file_path = os.path.join(output_dir_path, "used_locators.json")
    with open(output_file_path, "w") as output_file:
        json.dump(merged_data, output_file, indent=4)


merge_ui_coverage_json_files(rootpath.detect() / Path("ui_coverage"), rootpath.detect())
