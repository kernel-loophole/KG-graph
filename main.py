from graph_gen import main_kg
from graph_gen import main_ner
from find_ner import ner_finder
from difference import diff_graph
from ner_plot import ner_plotter
main_ner.main_ner()
main_kg.main_kg()
diff_graph()
ner_finder()
ner_plotter()