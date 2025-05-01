import pandas as pd

def test_input_shape():
    # Example: Load a CSV used in your repo
    df = pd.read_csv("../data/combined_all_employees_salaries_cleaned.csv")  # change path if needed
    assert df.shape[1] > 0, "Data has no columns"
    assert df.shape[0] > 0, "Data has no rows"
    # (318411, 13) Only check 13 columns
    assert df.shape[1] == 13, f"Expected 13 columns, got {df.shape[1]}"
    df2 = pd.read_csv("../data/Responsive_record2020.csv")  # change path if needed
    assert df2.shape[1] > 0, "Data has no columns"
    assert df2.shape[0] > 0, "Data has no rows"
    # (2229, 17)
    assert df2.shape[1] == 17, f"Expected 17 columns, got {df2.shape[1]}"