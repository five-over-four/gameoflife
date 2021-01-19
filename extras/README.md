# GIF Generation
## Generating PNG images
First, initialise `filename = 0` in the game function, outside the while loop. Next,  
paste the following code anywhere inside the loop:

    if timer == 0:
        pygame.image.save(screen, str(filename) + ".png")
        filename += 1

## PNG to GIF
The .gif itself was generated with the following code. Note that the filenames must be "number.png" in format.

    import os
    import imageio

    dir = os.getcwd()
    image_folder = os.fsencode(dir)

    images = []

    for filename in os.listdir(dir):
        if filename.endswith(".png"):
            images.append(filename)

    images = sorted(images, key = lambda x: int(x.split(".")[0]))
    imgs = list(map(lambda filename: imageio.imread(filename), images))

    imageio.mimsave(os.path.join('sample.gif'), imgs, duration = 0.1)

![A simple fork](https://raw.githubusercontent.com/not-legato/gameoflife/main/extras/sample_animation.gif)
