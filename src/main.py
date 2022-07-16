import cv2
import img_render.renderer

# TODO: validity checks
image = cv2.imread("test_source/img.jpg")

targetWidth = 60 # future characters
# preserve aspect ratio
targetHeight = round(image.shape[1] * (targetWidth / image.shape[0]))
targetHeight = targetHeight
targetWidth *= 2 # TODO: figure something out about characters rendering

renderer = img_render.renderer.Renderer()

rendered = renderer.render(image, (targetWidth, targetHeight))
print(rendered)
