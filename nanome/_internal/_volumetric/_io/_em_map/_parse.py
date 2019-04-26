# from ..._volume_data import _VolumeData
class _VolumeData(object):
    def __init__(self, 
                 size_x, size_y, size_z, 
                 delta_x, delta_y, delta_z):
        self._data = []        

        self._size_x = size_x
        self._size_y = size_y
        self._size_z = size_z
        
        self._delta_x = delta_x
        self._delta_y = delta_y
        self._delta_z = delta_z

        self._origin_x = 0.0
        self._origin_y = 0.0
        self._origin_z = 0.0

import struct

float_unpack = struct.Struct('!f').unpack_from
int_unpack = struct.Struct('!i').unpack_from

def parse_file(path):
    try:
        data = []
        with open(path, mode='rb') as f:
            data = f.read()
        if data == []:
            return None
        result = parse_data(data)
        return result
    except:
        print("Could not read pdb file: " + path)
        raise

# def read_float(self):
#     pre = self._buffered_computed
#     result = _Data.int_unpack(self._received_bytes, pre)[0]
#     self.consume_data(4)
#     return result

def read_buffer(bytes):
    header_size = 1024
    header = struct.unpack(str(256)+"i", bytes[:header_size])
    unit_cell = struct.unpack(str(6)+"f", bytes[40:64])
    symmetry_size = header[23]
    symmetry = bytes[header_size:symmetry_size]
    body = bytes[header_size+symmetry_size:]
    return header, unit_cell, symmetry, body

def parse_data(bytes):
    results = read_buffer(bytes)
    header, unit_cell, symmetry_size, body = results
    if (header[52] != 0x2050414d):
        if (header[52] == 0x4d415020):
            raise Exception("CryoEM> File is encoded on a big-endian machine")
        raise Exception("CryoEM> File doesn't have proper header")
    n_columns = header[0]
    n_rows = header[1]
    n_section = header[2]
    mode = header[3]
    data_size_byte = 0
    if (mode == 2):
        data_size_byte = 4
    else:
        raise Exception("CryoEM> Only mode 2 is supported")
    
    start_x = header[4]
    start_y = header[5]
    start_z = header[6]
    
    if (unit_cell[3] != 90 or unit_cell[4] != 90 or unit_cell[5] != 90):
        raise ("CryoEM> Cell is not perpendicular. Is this an Electron Density Map?")

    delta_x = unit_cell[0] / header[7]
    delta_y = unit_cell[1] / header[8]
    delta_z = unit_cell[2] / header[9]
    map = _VolumeData(n_columns, n_rows, n_section, delta_x, delta_y, delta_z)
    if (header[16] != 1 or header[17] != 2 or header[18] != 3):
        raise Exception("CryoEM> data layout doesn't meet Cryo-EM standard. Is this an Electron Density Map?")
    symmetrySizeByte = header[23]
    if (symmetrySizeByte != 0):
        raise Exception("CryoEM> contains symmetry operation.")
    map.data = body

    return map

import os 
dir_path = os.path.dirname(os.path.realpath(__file__)) + "/test.map"
with open(dir_path, mode='rb') as f:
    data = f.read()
    map = parse_data(data)
    print("deltas: ", str(map._delta_x), str(map._delta_y), str(map._delta_z))
    print("deltas: ", str(map._size_x), str(map._size_y), str(map._size_z))
