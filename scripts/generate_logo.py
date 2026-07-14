from PIL import Image, ImageDraw

WIDTH = 128
HEIGHT = 128

bg_color = (11, 95, 196, 255)  # #0b5fc4
sun_center = (46, 54)
SUN_R = 16
cloud_color = (223, 244, 255, 255)  # light blue-white
cloud_shadow = (159, 198, 255, 255)
base_accent = (111, 143, 184, 230)

im = Image.new('RGBA', (WIDTH, HEIGHT), bg_color)
d = ImageDraw.Draw(im)

# Draw simple sun (radial-like by concentric circles)
for i, c in enumerate([(255,210,77,255),(255,154,60,200),(255,154,60,120)]):
    r = SUN_R - i*5
    if r>0:
        bbox = [sun_center[0]-r, sun_center[1]-r, sun_center[0]+r, sun_center[1]+r]
        d.ellipse(bbox, fill=c)

# Draw cloud overlapping sun (in front)
# Draw multiple ellipses to form a cloud shape
cloud_ellipses = [
    (34, 58, 74, 90),
    (50, 48, 94, 86),
    (20, 66, 60, 94)
]
for bbox in cloud_ellipses:
    d.ellipse(bbox, fill=cloud_color)

# Add a brighter top highlight
d.ellipse((46,50,86,80), fill=cloud_shadow)

# Base accent bar
d.rounded_rectangle((40, 92, 88, 112), radius=6, fill=base_accent)

# Save to repo root and component folder
im.save('../logo.png')
im.save('../custom_components/kraichtal_wetter_api/logo.png')
print('Generated logo.png and custom_components/.../logo.png')
