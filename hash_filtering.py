import pandas as pd
import numpy as np
import hashlib  # For MD5 hashing

# Simulating large datasets
num_records = 7_000_000

# Generating old_df
old_df = pd.DataFrame({
    'address': np.random.choice(['123 Main St', '456 Oak St', '789 Pine St'], num_records),
    'city': np.random.choice(['New York', 'Los Angeles', 'San Francisco'], num_records),
    'zip': np.random.choice(['10001', '90001', '94101'], num_records),
    'as_of_date': np.random.choice(['2024-01-01', '2024-01-02'], num_records)
})

# Generating new_df (with some new addresses)
new_df = pd.DataFrame({
    'address': np.random.choice(['456 Oak St', '789 Pine St', '101 Maple St'], num_records),
    'city': np.random.choice(['Los Angeles', 'San Francisco', 'Chicago'], num_records),
    'zip': np.random.choice(['90001', '94101', '60601'], num_records),
    'as_of_date': np.random.choice(['2024-02-01', '2024-02-02'], num_records)
})

# 🚀 Step 1: Create full address field
def create_full_address(df):
    return df['address'] + ', ' + df['city'] + ', ' + df['zip']

old_df['full_address'] = create_full_address(old_df)
new_df['full_address'] = create_full_address(new_df)

# 🚀 Step 2: Compute MD5 hashes (vectorized with NumPy)
def hash_md5_np(array):
    """Vectorized MD5 hashing using NumPy."""
    return np.array([hashlib.md5(addr.encode()).hexdigest() for addr in array])

# Compute hashes for old and new addresses
old_hashes = hash_md5_np(old_df['full_address'].to_numpy())
new_hashes = hash_md5_np(new_df['full_address'].to_numpy())

# 🚀 Step 3: Convert old_hashes to a set for O(1) lookups
old_hash_set = set(old_hashes)

# 🚀 Step 4: Use list comprehension for fast filtering
new_mask = np.array([h not in old_hash_set for h in new_hashes])

# 🚀 Step 5: Filter new_df
new_only_df = new_df.iloc[new_mask]

print(new_only_df.shape)  # Output count of new addresses 


#Pytest

import pandas as pd
import pytest
from datapuller import DataPuller

@pytest.fixture
def test_data():
    """Creates sample old and new DataFrames for testing."""
    old_df = pd.DataFrame({
        'address': ['123 Main St', '456 Oak St'],
        'city': ['New York', 'Los Angeles'],
        'zip': ['10001', '90001'],
        'as_of_date': ['2024-01-01', '2024-01-02']
    })

    new_df = pd.DataFrame({
        'address': ['456 Oak St', '789 Pine St'],
        'city': ['Los Angeles', 'San Francisco'],
        'zip': ['90001', '94101'],
        'as_of_date': ['2024-02-01', '2024-02-02']
    })

    return old_df, new_df

def test_create_full_address(test_data):
    """Tests if full address is created correctly."""
    old_df, new_df = test_data
    dp = DataPuller(old_df, new_df)

    full_address = dp.create_full_address(old_df)
    expected = pd.Series(['123 Main St, New York, 10001', '456 Oak St, Los Angeles, 90001'])

    pd.testing.assert_series_equal(full_address, expected)

def test_get_new_addresses(test_data):
    """Tests if new addresses are identified correctly."""
    old_df, new_df = test_data
    dp = DataPuller(old_df, new_df)
    new_only_df = dp.get_new_addresses()

    # Expected new address
    expected_df = pd.DataFrame({
        'address': ['789 Pine St'],
        'city': ['San Francisco'],
        'zip': ['94101'],
        'as_of_date': ['2024-02-02'],
        'full_address': ['789 Pine St, San Francisco, 94101']
    })

    pd.testing.assert_frame_equal(new_only_df.reset_index(drop=True), expected_df)

def test_performance():
    """Tests if function runs efficiently on large data."""
    num_records = 1_000_000  # 1 million rows for testing

    old_df = pd.DataFrame({
        'address': ['123 Main St'] * num_records,
        'city': ['New York'] * num_records,
        'zip': ['10001'] * num_records,
        'as_of_date': ['2024-01-01'] * num_records
    })

    new_df = pd.DataFrame({
        'address': ['456 Oak St'] * num_records,
        'city': ['Los Angeles'] * num_records,
        'zip': ['90001'] * num_records,
        'as_of_date': ['2024-02-01'] * num_records
    })

    dp = DataPuller(old_df, new_df)

    import time
    start_time = time.time()
    new_only_df = dp.get_new_addresses()
    end_time = time.time()

    # Ensure at least 1 new record is detected
    assert not new_only_df.empty

    # Check if function runs in under 2 seconds for 1M rows
    assert (end_time - start_time) < 2.0, "
