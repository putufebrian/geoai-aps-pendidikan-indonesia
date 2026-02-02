import sys
import os

# Tambahkan ROOT PROJECT ke PYTHONPATH
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from model.model_kebijakan_pendidikan import ModelKebijakanPendidikan
import pickle

model = ModelKebijakanPendidikan()

with open(os.path.join(BASE_DIR, "model", "model_kebijakan_pendidikan_2025.pkl"), "wb") as f:
    pickle.dump(model, f)

print("MODEL PKL BERHASIL DIBUAT")
