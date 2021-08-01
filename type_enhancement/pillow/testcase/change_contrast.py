from PIL import Image


def change_contrast(img, level):
    factor = (259 * (level + 255)) / (255 * (259 - level))

    def contrast(c):
        return int(128 + factor * (c - 128))

    return img.point(contrast)


if __name__ == "__main__":
    # Load image
    img = Image.open("image_data/lena.jpg")
    # Change contrast to 170
    cont_img = img.point(170)
    v1 = cont_img.save("image_data/lena_high_contrast.png", format="png")