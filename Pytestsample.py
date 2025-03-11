import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from your_package.module import split_and_store_dataframe
from your_package.storage import StorageFile  # Import the class being patched


@pytest.fixture
def mock_dataframe():
    """Creates a sample DataFrame for testing."""
    return pd.DataFrame({
        "id": [1, 2, 3, 4],
        "value": ["A", "B", "C", "D"],
        "data": [10, 20, 30, 40]
    })


def test_split_and_store_dataframe(mock_dataframe):
    dataset_names = ["dataset_part1.parquet", "dataset_part2.parquet"]

    # Create a mock StorageFile instance
    mock_storage_instance = MagicMock()

    # Patch StorageFile to return a mock instance when used in a context manager
    with patch.object(StorageFile, "__enter__", return_value=mock_storage_instance):
        # Call the function under test
        split_and_store_dataframe(mock_dataframe, dataset_names)

        # Expected splits based on dataset names count
        num_splits = len(dataset_names)
        splits = [mock_dataframe.iloc[i::num_splits] for i in range(num_splits)]

        # Verify `write_object` was called correctly for each split
        expected_calls = [((mock_storage_instance, split, name),) for split, name in zip(splits, dataset_names)]
        mock_storage_instance.write_object.assert_has_calls(expected_calls, any_order=True)

        # Ensure `write_object` was called the expected number of times
        assert mock_storage_instance.write_object.call_count == len(dataset_names)




###££

import pytest
import pandas as pd
from unittest.mock import patch
from process_data import process_data
from storage_grid import StorageGrid

def test_process_data():
    input_path = "input.csv"
    output_path = "output.csv"

    # Create a mock DataFrame for read_df to return
    mock_df = pd.DataFrame({"existing_col": [1, 2, 3]})

    with patch.object(StorageGrid, "read_df", return_value=mock_df) as mock_read, \
         patch.object(StorageGrid, "write_df") as mock_write:

        process_data(input_path, output_path)

        # Assert read_df was called with correct arguments
        mock_read.assert_called_once_with(input_path)

        # Capture the DataFrame passed to write_df
        args, _ = mock_write.call_args
        written_df = args[1]  # The second argument is the DataFrame

        # Assert the transformation happened correctly
        expected_df = mock_df.copy()
        expected_df["new_col"] = expected_df["existing_col"] * 2
        pd.testing.assert_frame_equal(written_df, expected_df)

        # Assert write_df was called with correct arguments
        mock_write.assert_called_once_with(output_path, expected_df)



#####
import pytest
import pandas as pd
from unittest.mock import MagicMock, patch
from process_data import process_data
from storage_grid import StorageGrid

def test_process_data():
    input_path = "input.csv"
    output_path = "output.csv"

    # Create a mock DataFrame for read_df to return
    mock_df = pd.DataFrame({"existing_col": [1, 2, 3]})

    # Create a MagicMock for StorageGrid
    mock_storage = MagicMock(spec=StorageGrid)
    mock_storage.__enter__.return_value = mock_storage  # Context manager behavior
    mock_storage.read_df.return_value = mock_df

    with patch("storage_grid.StorageGrid", return_value=mock_storage):
        process_data(input_path, output_path)

        # Ensure read_df was called with the correct argument
        mock_storage.read_df.assert_called_once_with(input_path)

        # Capture the DataFrame passed to write_df
        args, _ = mock_storage.write_df.call_args
        written_df = args[1]  # The second argument is the DataFrame

        # Assert the transformation happened correctly
        expected_df = mock_df.copy()
        expected_df["new_col"] = expected_df["existing_col"] * 2
        pd.testing.assert_frame_equal(written_df, expected_df)

        # Ensure write_df was called with the correct argument
        mock_storage.write_df.assert_called_once_with(output_path, expected_df)
