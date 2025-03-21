#!/bin/bash

echo "🔍 Checking Conda installation path..."

# Detect Conda installation path
CONDA_PATH=$(conda info --base 2>/dev/null)
EXPECTED_PATH="/opt/conda"  # Adjust this if needed

if [[ -z "$CONDA_PATH" ]]; then
    echo "❌ Conda not found! Make sure it's installed."
    exit 1
fi

echo "✅ Conda found at: $CONDA_PATH"

# Check if the path is incorrect (e.g., pointing to Miniconda)
if [[ "$CONDA_PATH" == *"miniconda"* ]]; then
    echo "❌ Incorrect Conda path detected: $CONDA_PATH"
    echo "🔄 Updating to expected path: $EXPECTED_PATH"
    export CONDA_PREFIX=$EXPECTED_PATH
else
    export CONDA_PREFIX=$CONDA_PATH
fi

# Set necessary environment variables
echo "🔧 Setting required paths..."
export PATH=$CONDA_PREFIX/bin:$PATH
export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$LD_LIBRARY_PATH

# Verify paths are correctly set
echo "🛠 Verifying setup..."
echo "CONDA_PREFIX: $CONDA_PREFIX"
echo "PATH: $PATH"
echo "LD_LIBRARY_PATH: $LD_LIBRARY_PATH"

# Persist settings for builds
echo "📌 Saving settings to environment files..."

echo "export CONDA_PREFIX=$CONDA_PREFIX" >> ~/.bashrc
echo "export PATH=$CONDA_PREFIX/bin:\$PATH" >> ~/.bashrc
echo "export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:\$LD_LIBRARY_PATH" >> ~/.bashrc

echo "export CONDA_PREFIX=$CONDA_PREFIX" >> ~/.Renviron
echo "export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:\$LD_LIBRARY_PATH" >> ~/.Renviron

echo "✅ Conda environment setup completed!"


#######
before_script:
  - export CONDA_PREFIX=/opt/conda
  - export R_HOME=$CONDA_PREFIX/envs/r_env/lib/R
  - export R_LIBS_USER=$CONDA_PREFIX/envs/r_env/lib/R/library
  - export PATH=$CONDA_PREFIX/bin:$PATH
  - export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$LD_LIBRARY_PATH
