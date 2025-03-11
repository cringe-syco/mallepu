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
