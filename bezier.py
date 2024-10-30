import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
from scipy.special import comb

# Configuration parameters
BEZIER_DEGREE = 3  # Degree of the Bezier curve
BEZIER_RESOLUTION = 10000  # Number of points to generate on the Bezier curve
BACKGROUND_IMAGE_PATH = "screenshots/bezier.png"  # Path to the background image
LINE_COLOR = "red"  # Color of the drawing line
LINE_WIDTH = 2  # Width of the drawing line
CONTROL_POINT_STYLE = "k--o"  # Style for control points (black dashed line with dots)
ORIGINAL_POINT_STYLE = "ro"  # Style for original points (red dots)
CURVE_STYLE = "b-"  # Style for Bezier curve (solid blue line)

# Visualization settings
DARK_MODE = True  # Toggle dark mode
FIGURE_SIZE = (16, 9)  # Default figure size
FONT_SIZE = 16  # Default font size
VECTOR_ALPHA = 0.4  # Transparency for vector lines
VECTOR_HEAD_SIZE = 0.01  # Size of arrow heads
T_VALUE = 0.5  # The t value (0-1) for which to show the bias vectors for.

# Configure plot style
if DARK_MODE:
    plt.style.use("dark_background")
    CURVE_STYLE = "w--"  # White dashed line in dark mode
else:
    plt.style.use("default")

# Configure font sizes
plt.rc("font", size=FONT_SIZE)
plt.rc("axes", titlesize=FONT_SIZE, labelsize=FONT_SIZE)
plt.rc("xtick", labelsize=FONT_SIZE)
plt.rc("ytick", labelsize=FONT_SIZE)
plt.rc("legend", fontsize=FONT_SIZE)
plt.rc("figure", titlesize=FONT_SIZE)


class BezierCurveDrawer:
    """Class to handle drawing and capturing mouse events for the Bezier curve."""

    def __init__(self, line):
        self.line = line
        self.point_coords_x = []
        self.point_coords_y = []
        self.drawing_active = False

        # Connect matplotlib events to class methods
        self.connect_events()

    def connect_events(self):
        """Connect matplotlib events to their respective handlers."""
        fig = self.line.figure
        self.press_event = fig.canvas.mpl_connect("button_press_event", self.on_press)
        self.release_event = fig.canvas.mpl_connect(
            "button_release_event", self.on_release
        )
        self.motion_event = fig.canvas.mpl_connect(
            "motion_notify_event", self.on_motion
        )

    def on_press(self, event):
        """Handle mouse button press event."""
        if event.inaxes != self.line.axes:
            return
        self.drawing_active = True
        self.add_point(event.xdata, event.ydata)

    def on_release(self, event):
        """Handle mouse button release event."""
        self.drawing_active = False

    def on_motion(self, event):
        """Handle mouse motion event."""
        if not self.drawing_active or event.inaxes != self.line.axes:
            return
        self.add_point(event.xdata, event.ydata)

    def add_point(self, x, y):
        """Add a new point to the curve and update the display."""
        self.point_coords_x.append(x)
        self.point_coords_y.append(y)
        self.line.set_data(self.point_coords_x, self.point_coords_y)
        self.line.figure.canvas.draw()


def bernstein_polynomial(i, n, t):
    """
    Calculate the Bernstein polynomial value.

    Args:
        i (int): Index of the control point
        n (int): Degree of the polynomial
        t (float or array): Parameter value(s) between 0 and 1

    Returns:
        float or array: Bernstein polynomial value(s)
    """
    return comb(n, i) * t**i * (1 - t) ** (n - i)


def calculate_bezier_parameters(x_coords, y_coords, degree=BEZIER_DEGREE):
    """
    Calculate the control points for a Bezier curve fitting the given points.

    Args:
        x_coords (list): X coordinates of the points
        y_coords (list): Y coordinates of the points
        degree (int): Degree of the Bezier curve

    Returns:
        list: Control points for the Bezier curve
    """
    # Input validation
    if degree < 1:
        raise ValueError("Degree must be 1 or greater.")
    if len(x_coords) != len(y_coords):
        raise ValueError("X and Y coordinates must have the same length.")
    if len(x_coords) < degree + 1:
        raise ValueError(
            f"Need at least {degree + 1} points for degree {degree} curve."
        )

    def create_bernstein_matrix(t_values):
        """Create the Bernstein matrix for the given t values."""
        return np.matrix(
            [
                [bernstein_polynomial(k, degree, t) for k in range(degree + 1)]
                for t in t_values
            ]
        )

    # Calculate parameters
    t_values = np.linspace(0, 1, len(x_coords))
    bernstein_matrix = create_bernstein_matrix(t_values)
    points = np.array(list(zip(x_coords, y_coords)))

    # Compute control points using least squares fitting
    matrix_pinv = np.linalg.pinv(bernstein_matrix)
    control_points = (matrix_pinv * points).tolist()

    # Ensure first and last points match the input
    control_points[0] = [x_coords[0], y_coords[0]]
    control_points[-1] = [x_coords[-1], y_coords[-1]]

    return control_points


def generate_bezier_curve(control_points, num_points=BEZIER_RESOLUTION):
    """
    Generate points along a Bezier curve defined by control points.

    Args:
        control_points (list): List of control point coordinates
        num_points (int): Number of points to generate along the curve

    Returns:
        tuple: Arrays of x and y coordinates of points on the curve
    """
    num_control_points = len(control_points)
    t_values = np.linspace(0.0, 1.0, num_points)

    # Calculate polynomial values for each control point
    polynomials = np.array(
        [
            bernstein_polynomial(i, num_control_points - 1, t_values)
            for i in range(num_control_points)
        ]
    )

    # Extract x and y coordinates from control points
    x_coords = np.array([p[0] for p in control_points])
    y_coords = np.array([p[1] for p in control_points])

    # Generate curve points
    curve_x = np.dot(x_coords, polynomials)
    curve_y = np.dot(y_coords, polynomials)

    return curve_x, curve_y


def setup_drawing_canvas(background_image_path):
    """
    Set up the matplotlib canvas for drawing with the background image.

    Args:
        background_image_path (str): Path to the background image file

    Returns:
        tuple: Points drawn by the user
    """
    # Load and process background image
    image = mpimg.imread(background_image_path)
    height, width, _ = image.shape
    aspect_ratio = width / height

    # Create figure and set up axes
    fig, ax = plt.subplots(figsize=(width / height, 1))
    ax.set_title("Trace of the Bezier curve")

    # Set plot limits based on aspect ratio
    if aspect_ratio >= 1:
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1 / aspect_ratio)
        ax.imshow(image, extent=[0, 1, 0, 1 / aspect_ratio], aspect="equal")
    else:
        ax.set_xlim(0, aspect_ratio)
        ax.set_ylim(0, 1)
        ax.imshow(image, extent=[0, aspect_ratio, 0, 1], aspect="equal")

    # Create line for drawing
    (line,) = ax.plot([], [], color=LINE_COLOR, linewidth=LINE_WIDTH)
    drawer = BezierCurveDrawer(line)

    plt.show()

    return list(zip(drawer.point_coords_x, drawer.point_coords_y))


def plot_bezier_results(original_points, control_points, curve_points, mse):
    """
    Plot the original points, control points, and the resulting Bezier curve.

    Args:
        original_points (tuple): Original x and y coordinates
        control_points (list): Control points of the Bezier curve
        curve_points (tuple): Points on the Bezier curve
        mse (float): Mean squared error of the fit
    """
    plt.figure(figsize=FIGURE_SIZE)

    # Extract coordinates
    orig_x, orig_y = zip(*original_points)
    control_x = [p[0] for p in control_points]
    control_y = [p[1] for p in control_points]
    curve_x, curve_y = curve_points

    # Plot original points and control points
    plt.plot(orig_x, orig_y, ORIGINAL_POINT_STYLE, label="Original Points")
    plt.plot(control_x, control_y, CONTROL_POINT_STYLE, label="Control Points")

    # Add control point annotations
    legend_elements = []
    for i, (x, y) in enumerate(zip(control_x, control_y)):
        plt.annotate(
            f"P{i}",
            (x, y),
            textcoords="offset points",
            xytext=(10 * (i % 2), 10 * (i % 2)),
            ha="center",
            fontsize=12,
        )
        legend_elements.append(
            plt.Line2D(
                [0],
                [0],
                marker="o",
                color="w",
                label=f"P{i}: ({x:.2f}, {y:.2f})",
                markerfacecolor="k",
                markersize=5,
            )
        )

    # Plot Bezier curve
    plt.plot(curve_x, curve_y, CURVE_STYLE, label="Bézier Curve")

    # Add legends
    ax = plt.gca()
    legend1 = plt.legend(
        title=f"Bézier Curve (degree={BEZIER_DEGREE})\nMSE: {mse:.2f}\n",
        loc="upper left",
    )
    ax.add_artist(legend1)
    plt.legend(handles=legend_elements, loc="lower right")

    plt.grid(True, alpha=0.2)
    plt.title("Fitted Bezier Curve")
    plt.xlabel("x")
    plt.ylabel("y")


def plot_bernstein_polynomials(degree=BEZIER_DEGREE):
    """
    Plot the Bernstein polynomials for the given degree.

    Args:
        degree (int): Degree of the Bernstein polynomials
    """
    # Generate colors for plotting
    colors = plt.cm.rainbow(np.linspace(0, 1, degree + 1))

    plt.figure(figsize=FIGURE_SIZE)

    # Plot individual Bernstein polynomials
    x_vals = np.linspace(0, 1, 100)
    for i in range(degree + 1):
        y_vals = bernstein_polynomial(i, degree, x_vals)
        plt.plot(
            x_vals,
            y_vals,
            label=f"$B_{{{degree},{i}}}(t)$",
            color=colors[i],
            linewidth=3,
        )

    # Plot the sum of Bernstein polynomials (partition of unity)
    y_vals_sum = np.ones_like(x_vals)
    plt.plot(
        x_vals,
        y_vals_sum,
        label="partition of unity",
        color="white" if DARK_MODE else "black",
        linewidth=2,
    )

    plt.legend(loc="lower right")
    plt.xlabel("t")
    plt.ylabel("B(t)")
    plt.title("Bernstein Polynomials")
    plt.grid(True, alpha=0.2)
    plt.show()


def plot_control_point_vectors(control_points, t_value=T_VALUE):
    """
    Plot vectors from origin to control points and their weighted combinations.

    Args:
        control_points (np.ndarray): Array of control point coordinates
        t_value (float): Parameter value along the curve (0 to 1)
    """
    n = len(control_points) - 1
    colors = plt.cm.rainbow(np.linspace(0, 1, n + 1))

    # Calculate coefficients at the given t value
    coeffs = [bernstein_polynomial(i, n, t_value) for i in range(n + 1)]

    plt.figure(figsize=FIGURE_SIZE)

    # Plot vectors from origin
    for i, point in enumerate(control_points):
        # Plot full vector (dotted)
        plt.arrow(
            0,
            0,
            point[0],
            point[1],
            head_width=0,
            head_length=0,
            fc=colors[i],
            ec=colors[i],
            linestyle=":",
            linewidth=2,
            alpha=VECTOR_ALPHA,
        )

        # Plot weighted vector (solid)
        plt.arrow(
            0,
            0,
            coeffs[i] * point[0],
            coeffs[i] * point[1],
            head_width=VECTOR_HEAD_SIZE,
            head_length=VECTOR_HEAD_SIZE,
            fc=colors[i],
            ec=colors[i],
        )

    # Plot control points
    plt.scatter(
        control_points[:, 0],
        control_points[:, 1],
        color=colors,
        edgecolors=colors,
        label="Control Points",
        linewidths=2,
    )

    # Annotate control points
    for i, (x, y) in enumerate(control_points):
        plt.annotate(
            f"P{i}",
            (x, y),
            textcoords="offset points",
            xytext=(-10, 10),
            ha="center",
            fontsize=10,
        )

    # Plot Bezier curve
    curve_points = generate_bezier_curve(control_points.tolist())
    plt.plot(
        curve_points[0], curve_points[1], CURVE_STYLE, label="Bezier Curve", alpha=0.8
    )

    plt.legend(loc="upper right")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(f"Vectors from Origin to Control Points (t={t_value:.2f})")
    plt.grid(True, alpha=0.2)
    plt.axis("equal")
    plt.show()


def plot_sequential_vectors(control_points, t_value=T_VALUE):
    """
    Plot vectors connecting sequentially with weights at a given t value.

    Args:
        control_points (np.ndarray): Array of control point coordinates
        t_value (float): Parameter value along the curve (0 to 1)
    """
    n = len(control_points) - 1
    colors = plt.cm.rainbow(np.linspace(0, 1, n + 1))

    # Calculate coefficients at the given t value
    coeffs = [bernstein_polynomial(i, n, t_value) for i in range(n + 1)]

    plt.figure(figsize=FIGURE_SIZE)

    # Draw sequential vectors
    start_point = np.array([0, 0])
    for i, point in enumerate(control_points):
        end_point = start_point + coeffs[i] * point
        plt.arrow(
            start_point[0],
            start_point[1],
            (end_point - start_point)[0],
            (end_point - start_point)[1],
            head_width=VECTOR_HEAD_SIZE,
            head_length=VECTOR_HEAD_SIZE,
            fc=colors[i],
            ec=colors[i],
        )
        start_point = end_point

    # Plot control points
    plt.scatter(
        control_points[:, 0],
        control_points[:, 1],
        color=colors,
        edgecolors=colors,
        label="Control Points",
        linewidths=2,
    )

    # Annotate control points
    for i, (x, y) in enumerate(control_points):
        plt.annotate(
            f"P{i}",
            (x, y),
            textcoords="offset points",
            xytext=(-10, 10),
            ha="center",
            fontsize=10,
        )

    # Plot Bezier curve
    curve_points = generate_bezier_curve(control_points.tolist())
    plt.plot(
        curve_points[0], curve_points[1], CURVE_STYLE, label="Bezier Curve", alpha=0.8
    )

    plt.legend(loc="upper right")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(f"Sequential Vector Addition (t={t_value:.2f})")
    plt.grid(True, alpha=0.2)
    plt.axis("equal")
    plt.show()


def main():
    """Main function to run the Bezier curve drawing and visualization process."""
    # Get user-drawn points
    drawn_points = setup_drawing_canvas(BACKGROUND_IMAGE_PATH)

    # Extract x and y coordinates
    x_coords, y_coords = zip(*drawn_points)

    # Calculate Bezier curve control points
    control_points = calculate_bezier_parameters(x_coords, y_coords, BEZIER_DEGREE)
    control_points_array = np.array(control_points)

    # Generate the Bezier curve
    curve_x, curve_y = generate_bezier_curve(control_points)

    # Calculate Mean Squared Error
    interp_func = interp1d(curve_x, curve_y, kind="linear", fill_value="interpolate")
    x_bounded = np.clip(x_coords, np.min(curve_x), np.max(curve_x))
    y_interpolated = interp_func(x_bounded)
    mse = np.mean((np.array(y_coords) - np.array(y_interpolated)) ** 2)

    # Plot results
    plot_bezier_results(drawn_points, control_points, (curve_x, curve_y), mse)
    plt.show()

    # Plot Bernstein polynomials
    plot_bernstein_polynomials(BEZIER_DEGREE)

    # Plot vector visualizations at t=0.5
    plot_control_point_vectors(control_points_array)
    plot_sequential_vectors(control_points_array)


if __name__ == "__main__":
    main()
