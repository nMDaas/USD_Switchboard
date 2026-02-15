import os
import sys

def run():
    folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    #check if folder is part of PYTHONPATH and if not, add it
    if folder not in sys.path:
        sys.path.append(folder)

    if 'src' in sys.modules:
        del sys.modules['src']
    if 'src.VariantAuthoringToolWrapper' in sys.modules:
        del sys.modules['src.VariantAuthoringToolWrapper']
    import src.VariantAuthoringToolWrapper

    return src.VariantAuthoringToolWrapper.executeUsdFileVariantAuthor()