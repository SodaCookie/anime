# anime
## Overview
The library defines a light declarative styled animation framework for the [pygame](http://pygame.org/news.html) library. It supports both [functional](#functional) and object-oriented paradigms.

## Installation
You can install this library from PyPI.
```
python -m pip install anime
pip install anime
```

## Requirements
* Python 3.x
* Pygame

## Usage
The library defines two main types to be used: `RubberBand` and `Anime`. However, when importing anime as `import anime`, only the Anime class is imported. To import RubberBand, import `anime.core.rubberband`.

### RubberBand
RubberBand defines how most classes in the library will behave. RubberBand is responsible for keeping track of its attributes' destinations and provides hooks for how those attributes will go towards their respective destinations. When an attribute in an instance of the class is mainipulated with the `__setattr__` operator and a Filter object is bound to the attribute, the attribute will be marked as dirty and the value that the attribute will be set to will be stored as a destination instead. Any attribute can be given a "Filter" which is a callable object that expects the attribute, its destination and current speed. When `instance.update` is called, the attributes current value will be passed through the filter and the new value of the attribute will be stored. Once the Filter's *done* method returns `True` given the new value, destination and speed, that attribute will be considered clean and no longer updated and set to its destination. For example:

##### Object Oriented
``` python
import anime.core.rubberband.RubberBand as RubberBand
from anime.core.filter import linear
instance = RubberBand()             # Create instance of RubberBand
instance.x = 0                      # Add attribute 'x' to instance (new attributes will simply be added)
instance.set_filter('x', linear, 3) # Bind filter to attribute 'x' with linear filter at speed 3
instance.x = 10                     # will set destination to 10; 'x' will remain 0
print(instance.x)                   # Prints 0
print(instance.get_dest('x'))       # Prints 10
instance.update()
print(instance.x)                   # Prints 3 (linear only allows a change of up to 3)
```

Alternatively, the same implementation can be done by in a functional style by simply using the objects as simple containers and calling the same filter without binding the filters to the attribute. Effectively, implementing what the update function handles. This can be useful at times because it allows a greater amount of control during the updating step. For instance, you can add flow control between applications of seperate filters.

##### Functional
``` python
import anime.core.rubberband.RubberBand as RubberBand
from anime.core.filter import linear
instance = RubberBand()             # Create instance of RubberBand
instance.x = 0                      # Add attribute 'x' to instance (new attributes will simply be added)
mydest = 10
print(instance.x)                   # Prints 0
instance.x = linear(instance.x, mydest, speed=3)
print(instance.x)                   # Prints 3
```

### Anime
Anime is a wrapper around RubberBand that handles rendering of a pygame Surface and well as adds attributes commonly used for animation: position, angle, size. It is possible to apply a filter to any of the class's attributes. It also implements 'renderers' which define how the image will be drawn for each attribute. For instance, the renderer for angle will return a properly the rotated image. Renderers are executed in the order they were applied to the object. Renderers take the attributes value and the image to be drawn and outputs the new image. If renderers for angle, width and height were applied in that order than image will be passed through those renderers in that order where the image of, chaining the inputs and outputs of each renderer. All anime objects are drawn with anchor at the center to allow smooth rotation.

``` python
...
screen = pygame.display.set_mode((640, 480))    # Create screen
image = pygame.load("image_i_know.jpeg")        # Load image
instance = anime.Anime(image, 0, 0)             # Create an instance of Anime (image, x, y)
instance.set_filter('x', linear, 50)             # Set filter
instance.x = 100
instance.render(screen)                         # Renders at position 0
instance.update()
instance.render(screen)                         # Renders at position 50
instance.update()
instance.render(screen)                         # Renders at position 100
...
```

### core.filter/core.reducer/core.renderer
`core.filter` defines prebuilt filters both as functions and classes. `core.reducer` defines prebuilt reducers. `core.renderer` defines prebuilt renderers.

### math module
Defines useful wrappers around RubberBand that allow easy manipulation of coordinate systems outside if Cartesian coordinates such as Polar and Parametric functions. This is useful when you want your Anime object to follow a specific path.

``` python
from anime.math.parametric import Parametric2D
import math
x = lambda t: math.cos(t)
y = lambda t: math.sin(t)
para = Parametric2D(x, y)
para.t = 100
print(para.get_pos()) # Returns cos(100), sin(100)
```

## Demos
To run the various demos that come with this package, simply import any demo from the module anime.demo. CUrrently, there are a total of 8 demos. Source code for the demos can be foud under `[PythonLibDirectory]/anime/demo/`.

``` python
# Will import the first and second demos
import anime.demo.demo1
import anime.demo.demo2
```

1. *Demo 1* shows basic implementation for the anime library. Click to move the square up and down.
2. *Demo 2* shows filters applied to attributes other than position (size). Click to enlarge or shrink the square.
3. *Demo 3* shows how filters are applied to children and how to io implement clicking an object. Click the red square to enlarge/shrink squares and click elsewhere to hide/show the outer square.
4. *Demo 4* shows how the library can be used to implement slightly more complex behaviours. Click a square to drag it, lift to let go of the square.
5. *Demo 5* shows using an image and clicking an object with alpha. Click the character to frow or shrink, click outside of the charater to rotate, press 'r' to reset the image.
6. *Demo 6* shows the library with many objects (200). All squares will "look" toward the cursor.
7. *Demo 7* shows use of Bezier curves. click to move the character along the curve, press r to toggle between quadratic and cubic curve.
8. *Demo 8* shows use of general parametric curves. Character will move along a [Butterfly Curve] (https://en.wikipedia.org/wiki/Butterfly_curve_%28transcendental%29).

## Contact
* **E-mail**: eric.quin.zhang@gmail.com
* **GitHub**: You should be on it
