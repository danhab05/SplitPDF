from pypdf import PdfReader, PdfWriter, Transformation
from copy import deepcopy
from pypdf.generic import RectangleObject

def split_each_page_in_two(input_path: str, output_path: str, direction: str = "vertical"):
    """
    Coupe chaque page en deux pages :
      - direction="vertical" : moitié gauche + moitié droite (par défaut).
    Conversion vectorielle (aucune rasterisation).
    """
    assert direction in {"vertical", "horizontal"}
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for p in reader.pages:
        w = float(p.mediabox.width)
        h = float(p.mediabox.height)

        if direction == "vertical":
            mid = w / 2.0

            # PARTIE GAUCHE
            left = deepcopy(p)
            left.mediabox = RectangleObject((0, 0, mid, h))
            left.cropbox  = RectangleObject((0, 0, mid, h))
            writer.add_page(left)

            # PARTIE DROITE (on translate le contenu puis on recadre)
            right = deepcopy(p)
            right.add_transformation(Transformation().translate(-mid, 0))
            right.mediabox = RectangleObject((0, 0, mid, h))
            right.cropbox  = RectangleObject((0, 0, mid, h))
            writer.add_page(right)

        else:  # non utilisé ici mais gardé pour clarté
            mid = h / 2.0
            bottom = deepcopy(p)
            bottom.mediabox = RectangleObject((0, 0, w, mid))
            bottom.cropbox  = RectangleObject((0, 0, w, mid))
            writer.add_page(bottom)

            top = deepcopy(p)
            top.add_transformation(Transformation().translate(0, -mid))
            top.mediabox = RectangleObject((0, 0, w, mid))
            top.cropbox  = RectangleObject((0, 0, w, mid))
            writer.add_page(top)

    with open(output_path, "wb") as f:
        writer.write(f)
