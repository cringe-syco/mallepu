#!/bin/bash

# =====================================
# === CONDA INSTALLATION & SETUP ===
# =====================================
echo "🐍 Installing Miniconda..."
cd /tmp
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
bash miniconda.sh -b -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"
source $HOME/miniconda/bin/activate
echo "✔️ Miniconda Installed!"
echo ""

# =====================================
# === CONDA BASICS ===
# =====================================
echo "🐍 Conda Version & Info"
conda --version
conda info
conda list -n base  # List packages in base environment
echo ""

echo "🐍 Conda Configuration"
conda config --set auto_update_conda false
conda config --set notify_outdated_conda false
conda config --add channels conda-forge
conda config --show
echo ""

# =====================================
# === CREATING CUSTOM ENVIRONMENT (Python + C + Java) ===
# =====================================
echo "🐍 Creating a Custom Environment with Python, C, and Java"

# Create an environment YAML file
cat <<EOF > environment.yml
name: dev_env
channels:
  - conda-forge
dependencies:
  - python=3.9
  - numpy
  - pandas
  - matplotlib
  - scipy
  - gcc  # C Compiler
  - gxx_linux-64  # C++ Compiler
  - make
  - openjdk=11  # Java
  - pip
  - pip:
      - flask
      - requests
EOF

# Create environment from YAML file
conda env create -f environment.yml
echo "✔️ Custom Conda environment 'dev_env' created!"
echo ""

# Activate the new environment
echo "🐍 Activating the environment"
conda activate dev_env
echo ""

# =====================================
# === SETTING JAVA & C COMPILERS ===
# =====================================
echo "🛠️ Setting up Java and C Paths"

# Set Java Path
export JAVA_HOME=$(conda info --envs | grep "dev_env" | awk '{print $2}')/lib/openjdk
export PATH=$JAVA_HOME/bin:$PATH
echo "✔️ Java configured. JAVA_HOME set to $JAVA_HOME"

# Set C Compiler Path
export CC=$(which gcc)
export CXX=$(which g++)
echo "✔️ C Compiler set to: $CC"
echo ""

# =====================================
# === ENVIRONMENT MANAGEMENT ===
# =====================================
echo "🐍 Managing Conda Environments"
conda env list
echo ""

echo "🐍 Cloning & Exporting Environments"
conda create --name backup_env --clone dev_env
conda env export > backup_env.yml
echo "✔️ Environment exported to backup_env.yml"
echo ""

echo "🐍 Listing Installed Packages & History"
conda list --explicit > packages.txt  # Save package list
conda list --revisions                # Show all environment changes
conda install --revision 2            # Rollback to revision 2
echo ""

echo "🐍 Deleting Environments"
conda deactivate
conda env remove -n dev_env
echo "✔️ Environment 'dev_env' removed!"
echo ""

# =====================================
# === USING CONDA WITH JUPYTER ===
# =====================================
echo "📓 Conda & Jupyter Notebook"
conda install -c conda-forge jupyter -y
jupyter notebook
echo ""

# =====================================
# === CONDA PACKAGE CACHING & CLEANUP ===
# =====================================
echo "🧹 Cleaning Up Conda"
conda clean --all -y
conda clean --packages -y  # Remove unused packages
conda clean --tarballs -y  # Remove downloaded tar files
echo ""

# =====================================
# === CONDA TROUBLESHOOTING ===
# =====================================
echo "🐍 Conda Troubleshooting"
conda update conda -y
conda update --all -y
conda repair  # Fix broken Conda installations
echo ""

echo "✔️ Conda Script Execution Completed!"
