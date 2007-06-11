from Kamaelia.UI.Pygame.Ticker import Ticker
from Kamaelia.Util.PureTransformer import PureTransformer
from Kamaelia.Chassis.Pipeline import Pipeline

def NiceTickerPrefab(**other_ticker_args):
    """Ticker that displays black text on a white background, and transforms
    any non-string arguments passed to it into strings.
    Do not pass in keywords text_height, line_spacing, background_colour,
    outline_colour, or text_colour."""
    return Pipeline(PureTransformer(lambda x: str(x)),
             Ticker(text_height=16, line_spacing=2,
                    background_colour=(255, 255, 245), text_colour=(10,10,10),
                    outline_colour = (0,0,0),
                    **other_ticker_args)
             )
