from __future__ import absolute_import

import os
import tempfile

import h5py
from keras.models import load_model, save_model


def save_model_to_hdf5_group(model, f):
    # Crează un director temporar în loc de un fișier temporar
    tempdir = tempfile.mkdtemp(prefix='_')
    tempfname = os.path.join(tempdir, 'model.h5')  # Nume de fișier în directorul temporar
    try:
        # Salvarea modelului în fișierul specificat
        save_model(model, tempfname)
        with h5py.File(tempfname, 'r') as serialized_model:
            root_item = serialized_model.get('/')
            serialized_model.copy(root_item, f, 'kerasmodel')
    finally:
        # Îndepărtarea directorului temporar și a tuturor fișierelor sale
        os.remove(tempfname)
        os.rmdir(tempdir)


def load_model_from_hdf5_group(f, custom_objects=None):
    # Extract the model into a temporary file. Then we can use Keras
    # load_model to read it.
    tempfd, tempfname = tempfile.mkstemp(prefix='tmp-kerasmodel')
    try:
        os.close(tempfd)
        with h5py.File(tempfname, 'w') as serialized_model:
            root_item = f.get('model')
            if root_item is None:
                raise ValueError("Grupul 'kerasmodel' nu a fost găsit în fișierul HDF5.")
            for attr_name, attr_value in root_item.attrs.items():
                serialized_model.attrs[attr_name] = attr_value
            for k in root_item.keys():
                f.copy(root_item.get(k), serialized_model, k)

        serialized_model.close()
        return load_model(tempfname, custom_objects=custom_objects)
    finally:
        os.unlink(tempfname)
