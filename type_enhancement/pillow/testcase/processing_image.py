import numpy as np
from PIL import Image
import torch.nn.functional as F


imgs = []
short_edge_length = ''
max_size=1
interp_method = "bilinear"

img_augs = []
for img in imgs:
    h, w = img.shape[:2]
    # later: provide list and randomly choose index for resize
    size = np.random.randint(short_edge_length[0], short_edge_length[1] + 1)
    if size == 0:
        v1 =  img
    scale = size * 1.0 / min(h, w)
    if h < w:
        newh, neww = size, scale * w
    else:
        newh, neww = scale * h, size
    if max(newh, neww) > max_size:
        scale = max_size * 1.0 / max(newh, neww)
        newh = newh * scale
        neww = neww * scale
    neww = int(neww + 0.5)
    newh = int(newh + 0.5)

    if img.dtype == np.uint8:
        pil_image = Image.fromarray(img)
        pil_image = pil_image.resize((neww, newh), Image.BILINEAR)
        img = np.asarray(pil_image)
    else:
        img = img.permute(2, 0, 1).unsqueeze(0)  # 3, 0, 1)  # hw(c) -> nchw
        img = F.interpolate(img, (newh, neww), mode=interp_method, align_corners=False).squeeze(0)
    img_augs.append(img)

v2 = img_augs