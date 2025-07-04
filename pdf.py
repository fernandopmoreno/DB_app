from fpdf import FPDF

from aux_functions import resource_path

# Modified PDF class to include a header with custom text
class PDF(FPDF):

    def __init__(self, texto_cabecera, orientation = "portrait", unit = "mm", format = "A4", font_cache_dir = "DEPRECATED"):
        super().__init__(orientation, unit, format, font_cache_dir)
        self.texto_cabecera = texto_cabecera

    def header(self):
        if 'DejaVu' not in self.fonts:
            self.add_font('DejaVu', '', 'fonts/DejaVuSans.ttf', uni=True)
        self.set_font('DejaVu', '', 12)
        self.set_text_color(0, 0, 0)
        #self.image(resource_path("images/logo.png"), x=12, y=10, h=16)
        self.set_xy(70, 11)
        self.multi_cell(0, 5, self.texto_cabecera, align="R")