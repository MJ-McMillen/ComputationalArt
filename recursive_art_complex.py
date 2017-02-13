""" THis is the computational art miniproject
#Idea: Use complex numbers in my random functions so I can use HSV.
1. HSV can be converted to RGB
for HSV you need a hue, saturation, and value. If I use complex numbers in my
functions, I can do HSV easily I think. I would think of them in polar coordinat
es where H is the angle, s is the magnitude. I am not sure how to represent
value yet mathamatically.

The old one generates three random functions, one for R, one for G, and one for B
This one does not do that. It generates two. One for HS and one for V

Not sure how good this is going to turn out.

What if I use A as x and b as y

Idea:
1. Build a random complex function. - At the end, convert to polar form. the
angle is the hue and the magnitude is the saturation

2. Build a real function. This random function will dictate value

3. Remap value onto 0,1, Same with magnitude.

4. Remap the HSV onto RGB colors


by MJ-McMillen
 """

import random
import math
import colorsys
from PIL import Image
import cmath
from inspect import signature

def build_random_function_real(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)

    """
    ["prod", ["x"], ["y"]]
    ["avg",["x"],["y"]]
    ["cos_pi",["x"]]
    ["sin_pi",["x"]]
    ["x"]#can only be called if min depth is one
    ["y"]#can only be called if min depth is one
    ["geomean",["x"],["y"]]
    ["arctan",["x"]]

    if max_depth == 1:
        return random.choice([["x"],["y"]])
        #guerenteed terminal case

    if min_depth == 1:
        function = random.choice(["x","y","prod", "avg", "cos_pi","sin_pi","geomean","arctan"])
        if function in ["x","y"]:
            return [function]
        if function in ["cos_pi","sin_pi"]:
            return [function, build_random_function_real((min_depth-1),(max_depth-1))]
        return [function, build_random_function_real((min_depth-1),(max_depth-1)), build_random_function_real((min_depth-1),(max_depth-1))]

    function = random.choice(["prod", "avg", "cos_pi","sin_pi","geomean","arctan"])
    if function in ["cos_pi","sin_pi"]:
        return [function, build_random_function_real((min_depth-1),(max_depth-1))]
    return [function, build_random_function_real((min_depth-1),(max_depth-1)), build_random_function_real((min_depth-1),(max_depth-1))]


    #prod(a,b) = a*b
    #avg(a,b) = 0.5 * (a+b)
    #cos_pi(a) = cos(pi*a)
    #sin_pi(a) = sin(pi*a)
    #x(a,b) = a
    #y(a,b) = b

def evaluate_random_function_real(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

    """
    if f[0] == "x":
        return x
    elif f[0] == "y":
        return y
    elif f[0] == "cos_pi":
        return math.cos(math.pi*evaluate_random_function_real(f[1],x,y))
    elif f[0] == "sin_pi":
        return math.sin(math.pi*evaluate_random_function_real(f[1],x,y))
    elif f[0] == "prod":
        return evaluate_random_function_real(f[1],x,y)*evaluate_random_function_real(f[2],x,y)
    elif f[0] == "avg":
        return (evaluate_random_function_real(f[1],x,y)+evaluate_random_function_real(f[2],x,y))/2
    elif f[0] == "arctan":
        a2 = evaluate_random_function_real(f[1],x,y)
        return math.atan(evaluate_random_function_real(f[1],x,y)/a2)/(math.pi/2) if a2!=0  else 0
    elif f[0] == "geomean":
        a1 = evaluate_random_function_real(f[1],x,y)
        a2 = evaluate_random_function_real(f[2],x,y)
        return math.copysign(math.sqrt(math.fabs(a1*a2)),a1*a2)

#prod(a,b) = a*b
#avg(a,b) = 0.5 * (a+b)
#cos_pi(a) = cos(pi*a)
#sin_pi(a) = sin(pi*a)
#x(a,b) = a
#y(a,b) = b


def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    #needs to scale inupt into a different range.
    input_interval = abs(input_interval_end- input_interval_start)
    #the range of numbers input interval is 0 refed
    output_interval = abs(output_interval_end - output_interval_start)
    #the range of numbers the output interval is. 0 refed
    deltoval = val- input_interval_start
    scaled_val = (deltoval/input_interval)* output_interval
    return(output_interval_start + scaled_val)
#"exp" : (lambda c:cmath.exp(c))

functions = {"sum": (lambda c1,c2:c1+c2),"mult": (lambda c1,c2:c1*c2), "cos" : (lambda c:cmath.cos(c))}
allFunctions = {"I": "I"}
allFunctions.update(functions)

def build_random_function_imaginary(min_depth,max_depth):
    """ This function builds an imaginary function that can be used for HSV

    """
    if max_depth == 1:
        return ["I"]
    elif min_depth == 1:
        functionDict = allFunctions
    else:
        functionDict = functions
    functionName = random.choice(list(functionDict.keys()))
    function = functionDict[functionName]
    if function != "I":
        nParams = len(signature(function).parameters)
        params = [build_random_function_imaginary(min_depth-1,max_depth-1) for _ in range(nParams)]
        return [function] + params
    else:
        return [function]

def evaluate_random_function_imaginary(f, c):
    """This function evaluates the randomly generated imaginary function.
    It first goes through in a a+bi manner evaluating based on real and imaginary
    components. It outputs the real component and the imaginary one.

    NOT NOWx is a complex number a+bi where a =x and b = y
    y is a complex number a+bi where a = y and b =x
    """
    if f[0] == "I":
        return c
    return f[0](*[evaluate_random_function_imaginary(g,c) for g in f[1:]])

def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def HSV_to_RGB(c):
    """This function takes the HSV values and converts them to RGB values
    """
    H = math.degrees(cmath.phase(c))
    V = 1+(math.atan(abs(c))/(math.pi/2))
    return colorsys.hsv_to_rgb(H,1,V)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    HS = build_random_function_imaginary(4,4)
    #V = build_random_function_real(2,10)


    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            HS_evaled = evaluate_random_function_imaginary(HS,complex(x,y))
            #print(HS_evaled)
            #V_evaled =  evaluate_random_function_real(V,x,y)
            RGB = HSV_to_RGB(HS_evaled)
            pixels[i, j] = (
                color_map(RGB[0]),
                color_map(RGB[1]),
                color_map(RGB[2])
            )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    # generate_art("myart.png")

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    generate_art("myartcomp2.png")
