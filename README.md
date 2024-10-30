# Bezier Curve Visualization Tool

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Black](https://img.shields.io/badge/code%20style-black-000000.svg)
![isort](https://img.shields.io/badge/imports-isort-1674b1?style=flat&labelColor=ef8336)
![Matplotlib](https://img.shields.io/badge/matplotlib-3.7%2B-blue)

A comprehensive visualization tool for understanding and interacting with Bezier curves. This tool allows users to draw curves, visualize Bernstein polynomials, and understand the mathematical concepts behind Bezier curves through interactive visualizations.

<div style="text-align: center;">
  <img src="assets/bezier.jfif" alt="Bezier Curve Visualization Tool" width="300" height="300">
</div>

## Acknowledgements
Thank you to the following resources for providing valuable information for this project:
https://en.wikipedia.org/wiki/B%C3%A9zier_curve

Parts adapted and ported from Sage to Python from https://commons.wikimedia.org/wiki/File:Bernstein_poly_4.svg

To https://github.com/jegork/dysgraphia/blob/7edffa08a5c08571aeb080a625792797981d0607/bezier.py for the Bezier curve fitting algorithm

Finally, thank you to the [Freya Holmér](https://www.youtube.com/@acegikmo) for providing inspiration for this project which was used in my International Baccalaurate Mathematics Internal Assessment (and that 7!1!1!). The video can be found here:
https://www.youtube.com/watch?v=aVwxzDHniEw

## Description

This tool provides several key features for understanding and working with Bezier curves:

1. Interactive Drawing Tool
   - Draw curves directly on a canvas
   - Automatic fitting of Bezier curves to drawn points
   - Real-time visualization of control points

2. Bernstein Polynomial Visualization
   - View the individual Bernstein basis functions
   - See the partition of unity property
   - Interactive plots with customizable degree

3. Vector Visualization
   - View control point influence through vector visualization
   - See sequential vector addition at any point along the curve
   - Interactive visualization of curve construction

4. Dark Mode Support
   - Full dark mode support for all visualizations
   - Configurable styling options

## How to Use

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Wayrion/Bezier-Fitter.git
cd Bezier-Fitter
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

### Running the Tool

1. Basic Usage:
```python
python bezier_visualization.py
```

2. Interactive Drawing:
   - Click and drag on the canvas to draw a curve
   - Release to complete the drawing
   - The tool will automatically fit a Bezier curve to your drawing

3. Viewing Visualizations:
   - After drawing, the tool will show:
     - Your original curve with fitted Bezier curve
     - Bernstein polynomial basis functions
     - Vector visualizations at t=0.5

### Configuration

You can modify the following parameters in the script:

```python
# Basic Configuration
BEZIER_DEGREE = 3  # Change the degree of the Bezier curve
BEZIER_RESOLUTION = 10000  # Adjust curve resolution
DARK_MODE = True  # Toggle dark mode

# Visualization Settings
FIGURE_SIZE = (8, 6)  # Change plot size
FONT_SIZE = 16  # Adjust font size
VECTOR_ALPHA = 0.4  # Modify vector transparency
```

## Examples

### Drawing Mode
1. Start the program
2. Click and drag to draw your curve
3. Release to see the fitted Bezier curve

### Visualization Mode
After drawing, you'll see:
- The original points and fitted curve
- Control points with annotations
- Mean Squared Error (MSE) of the fit

### Mathematical Visualization
The tool will display:
- Bernstein polynomials for your curve's degree
- Vector influences at t=0.5
- Sequential vector addition visualization

## Requirements

- Python 3.8+
- NumPy
- Matplotlib
- SciPy

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Run `black` and `isort` on your code
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.