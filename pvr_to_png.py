##
import re
import png
import os
import pathlib

## Load File
def load_file(fname):
    in_file = open(fname, "rb") # rb read binary
    data = in_file.read()
    in_file.close()
    return data

## Find PVRT data index
def get_pvrt_index(data):
    ind = []
    for i in re.finditer(b'PVRT', data):
        ind.append(i.start())
    return ind

## Extract PVR files
def get_pvr_data(data, pvrt_index):
    offset_size = 4
    length_size = 4
    offset_data = 48
    pvr_data = []
    for i in pvrt_index:
        size_bytes = data[i + offset_size : i + offset_size + length_size]
        length_data = int.from_bytes(size_bytes, 'little', signed=False)
        # additional offset for mysterious blank data
        for j in range(i + offset_data + 3, i + offset_data + length_data, 4):
            if data[j] != 0:
                offset_data += (j - i - offset_data - 3)
                break

        pvr_data.append(data[i + offset_data : i + offset_data + length_data])
    return pvr_data

## Get pvr images
def get_pvr_images(pvr_data):
    w = 256
    moser = [0, 1, 4, 5, 16, 17, 20, 21, 64, 65, 68, 69, 80, 81, 84, 85, 256, 257, 260, 261, 272, 273, 276, 277, 320,
             321, 324, 325, 336, 337, 340, 341, 1024, 1025, 1028, 1029, 1040, 1041, 1044, 1045, 1088, 1089, 1092, 1093,
             1104, 1105, 1108, 1109, 1280, 1281, 1284, 1285, 1296, 1297, 1300, 1301, 1344, 1345, 1348, 1349, 1360, 1361,
             1364, 1365, 4096, 4097, 4100, 4101, 4112, 4113, 4116, 4117, 4160, 4161, 4164, 4165, 4176, 4177, 4180, 4181,
             4352, 4353, 4356, 4357, 4368, 4369, 4372, 4373, 4416, 4417, 4420, 4421, 4432, 4433, 4436, 4437, 5120, 5121,
             5124, 5125, 5136, 5137, 5140, 5141, 5184, 5185, 5188, 5189, 5200, 5201, 5204, 5205, 5376, 5377, 5380, 5381,
             5392, 5393, 5396, 5397, 5440, 5441, 5444, 5445, 5456, 5457, 5460, 5461, 16384, 16385, 16388, 16389, 16400,
             16401, 16404, 16405, 16448, 16449, 16452, 16453, 16464, 16465, 16468, 16469, 16640, 16641, 16644, 16645,
             16656, 16657, 16660, 16661, 16704, 16705, 16708, 16709, 16720, 16721, 16724, 16725, 17408, 17409, 17412,
             17413, 17424, 17425, 17428, 17429, 17472, 17473, 17476, 17477, 17488, 17489, 17492, 17493, 17664, 17665,
             17668, 17669, 17680, 17681, 17684, 17685, 17728, 17729, 17732, 17733, 17744, 17745, 17748, 17749, 20480,
             20481, 20484, 20485, 20496, 20497, 20500, 20501, 20544, 20545, 20548, 20549, 20560, 20561, 20564, 20565,
             20736, 20737, 20740, 20741, 20752, 20753, 20756, 20757, 20800, 20801, 20804, 20805, 20816, 20817, 20820,
             20821, 21504, 21505, 21508, 21509, 21520, 21521, 21524, 21525, 21568, 21569, 21572, 21573, 21584, 21585,
             21588, 21589, 21760, 21761, 21764, 21765, 21776, 21777, 21780, 21781, 21824, 21825, 21828, 21829, 21840,
             21841, 21844, 21845, 21845]
    imgs = []
    for d in pvr_data:
        img = []
        for y in range(w):
            row = ()
            for x in range(w):
                ind = (moser[x] + 2 * moser[y]) * 4
                row += (int(d[ind + 2]), int(d[ind + 1]), int(d[ind + 0]))
            img.append(row)
        imgs.append(img)
    return imgs

## Stitch images together
def stitch_images(imgs):
    w = 256
    img = []
    for i in range(0, 8, 2):
        for y in range(w):
            row = imgs[i][y] + imgs[i+1][y]
            img.append(row)
    return img

## Remove trailing whitespace
def remove_whitespace(img):
    n = len(img)
    for i in reversed(range(n)):
        if not set(img[i]).issubset((255, 0)):
            n = i+1
            break
    return img[0:n]

## Save image
def save_png(fname, img):
    w = int(len(img[0])/3)
    h = len(img)
    with open(fname, 'wb') as f:
        w = png.Writer(w, h, greyscale=False)
        w.write(f, img)

## Convert extracted pvm to image
def pvm_to_png(fname_in, fname_out):
    data = load_file(fname_in)
    pvrt_index = get_pvrt_index(data)
    pvr_data = get_pvr_data(data, pvrt_index)
    imgs = get_pvr_images(pvr_data)
    img = stitch_images(imgs)
    img = remove_whitespace(img)
    save_png(fname_out, img)

## Convert images
dir_in = pathlib.Path(r'C:\Users\pvm')
dir_out = pathlib.Path(r'C:\Users\png')

for f in os.listdir(dir_in):
    fname_in = dir_in.joinpath(f)
    fname_out = dir_out.joinpath(os.path.splitext(f)[0] + '.png')
    pvm_to_png(fname_in, fname_out)
