from this import d
from tkinter import Image
from tkinter.ttk import Progressbar
from skimage import measure
import skimage
import os
from skimage.io import imread, imshow, imread_collection, concatenate_images
import cv2
from skimage import img_as_uint,img_as_int,img_as_ubyte
import matplotlib.pyplot as plt
import numpy as np
import subprocess
import pandas
import napari
from magicgui import magic_factory
from qtpy.QtWidgets import QHBoxLayout, QPushButton, QWidget
from napari.types import ImageData, LabelsData, NewType
from skimage.transform import resize
from napari.utils.notifications import show_info
import pathlib
import tempfile
from zipfile import ZipFile
import os
from torch import _fake_quantize_learnable_per_tensor_affine
import conidie.path as paths
from magicgui import magicgui
import re
import PIL
import matplotlib.pyplot as plt
import numpy as np
from skimage import measure
import h5py
from skimage.filters import threshold_multiotsu
import napari
from os import listdir,makedirs
from os.path import isfile, join
from collections import Counter
from qtpy.QtWidgets import QListWidget
from skimage.measure import label
from magicgui.widgets import Table
from napari.types import ImageData, LabelsData, LayerDataTuple
from napari import Viewer
from pandas import DataFrame
from qtpy.QtWidgets import QTableWidget, QTableWidgetItem, QWidget, QGridLayout, QPushButton, QFileDialog
from skimage.measure import regionprops_table
import shutil
from magicgui import magicgui
import matplotlib.cm as cm
from fileinput import filename
from napari import layers
from glob import glob
from qtpy.QtWidgets import QListWidget
from qtpy.QtCore import Qt
from napari.utils import progress
from skimage.io import imsave
from napari.utils.colormaps import colormap_utils as cu
from collections import Counter
from magicgui.tqdm import trange

# from ilastik.experimental.api import from_project_file
import numpy
# from xarray import DataArray
import skimage.io
# from magicgui.tqdm import tmgrange, tqdm_mgui

colormap = cu.label_colormap()
colors = colormap.colors
color_dict = {}
color_dict[0] = colors[0]
color_dict[1] = colors[1]

zip_dir = tempfile.TemporaryDirectory()

#Structure du fichier compressé
#ZIP
#> dossier 1
#>> image
#>> mask
 
@magic_factory(call_button="Load images",filename={"label": "Pick a file:"})
def process_function_load(napari_viewer : Viewer,filename=pathlib.Path.cwd()): 
        
    with ZipFile(filename,'r') as zipObject:
            
        listOfFileNames = zipObject.namelist()
            
        for i in trange(len(listOfFileNames)):
            zipObject.extract(listOfFileNames[i],path=zip_dir.name)

    path_folder = zip_dir.name.replace("\\","/")
    folder = os.listdir(zip_dir.name.replace("\\","/"))[0]
    subfolder = os.listdir(path_folder+'/'+folder)

    A = []
    B = []

    for ix in range(len(subfolder)):
        if subfolder[ix].lower() == "image":
            image_folder = os.listdir(path_folder+'/'+folder+'/'+subfolder[ix])
            A = [path_folder+'/'+folder+'/'+subfolder[ix]+'/'+image_folder[i] for i in range(len(image_folder))]
        else:
            mask_folder = os.listdir(path_folder+'/'+folder+'/'+subfolder[ix])
            B = [path_folder+'/'+folder+'/'+subfolder[ix]+'/'+mask_folder[i] for i in range(len(mask_folder))]

    path_principal = path_folder+'/'+folder
    names =[]
    for i,j in zip(A,B):
        folder_name = i.split("/")[-1].split(".")[0]
        names.append(folder_name)
        
        os.mkdir(path_folder+'/'+folder_name)

        new_file = i.split('/')
        file_image = new_file[-1]
        new_file = path_folder+'/'+folder_name+'/'+file_image
        os.replace(i,new_file)

        new_file = j.split('/')
        file_image = new_file[-1]
        new_file = path_folder+'/'+folder_name+'/'+file_image
        os.replace(j,new_file)

    #effacer le dossier
    x1 = subfolder[0]
    x2 = subfolder[1]
    os.rmdir(path_principal+'/'+x1)
    os.rmdir(path_principal+'/'+x2)
    os.rmdir(path_principal)

    def open_name(item):
        
        name = item.text()
        name_folder = name[:-4]
    
        print('Loading', name, '...')

        napari_viewer.layers.select_all()
        napari_viewer.layers.remove_selected()    
        fname = f'{zip_dir.name}\{name}'
        for fname_i in os.listdir(fname):
            if fname_i.find('mask')!=-1:
                data_label = imread(f'{fname}\{fname_i}')
                data_label1 = np.array(data_label)
                non_fleur=np.where(data_label1==0)
                fleur=np.where(data_label1==255)
                data_label1[non_fleur]=0
                data_label1[fleur]=1
                
                napari_viewer.add_labels(data_label1,name=f'{fname_i[:-4]}')                
            else:
                napari_viewer.add_image(imread(f'{fname}\{fname_i}'),name=f'{fname_i[:-4]}')

        print('... done.')
    
    list_widget = QListWidget()
    for n in names:
        list_widget.addItem(n)    
    list_widget.currentItemChanged.connect(open_name)   
    napari_viewer.window.add_dock_widget([list_widget], area='right',name="Images")
    list_widget.setCurrentRow(0)
    
@magic_factory(call_button="save modification", layout="vertical")
def save_modification(image_seg : napari.layers.Labels, image_raw : ImageData, napari_viewer : Viewer):
    data_label = image_seg.data
    sousdossier = image_seg.name.split('_mask')[0]
    nom_image = image_seg.name.split('_mask')[1]
    os.remove(f'{zip_dir.name}\{sousdossier}\{image_seg}.png')
    classefleur=np.where(data_label==1)
    data_label[classefleur]=255
    imsave(f'{zip_dir.name}\{sousdossier}\{image_seg}.png',data_label)
    
@magic_factory(call_button="save zip",layout="vertical")
def save_as_zip():
    save_button = QPushButton("Save as zip")
    filename, _ = QFileDialog.getSaveFileName(save_button, "Save as zip", ".", "zip")
    shutil.make_archive(filename, 'zip', zip_dir.name)
    show_info('Compressed file done')