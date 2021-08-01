from PIL import Image


def change_brightness(img, level):
    def brightness(c):
        return 128 + level + (c - 128)

    if not -255.0 <= level <= 255.0:
        raise ValueError("level must be between -255.0 (black) and 255.0 (white)")
    return img.point(brightness)


if __name__ == "__main__":
    # Load image
    img = Image.open("image_data/lena.jpg")
    # Change brightness to 100
    brigt_img = img.point(128)
    v1 = brigt_img.save("image_data/lena_brightness.png", format="png")