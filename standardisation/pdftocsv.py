import importlib
import gmft
import gmft.table_detection
import gmft.table_visualization
import gmft.table_function
import gmft.table_function_algorithm
import gmft.table_captioning
import gmft.pdf_bindings.bindings_pdfium
import gmft.pdf_bindings
import gmft.common

importlib.reload(gmft)
importlib.reload(gmft.common)
importlib.reload(gmft.table_captioning)
importlib.reload(gmft.table_detection)
importlib.reload(gmft.table_visualization)
importlib.reload(gmft.table_function)
importlib.reload(gmft.table_function_algorithm)
importlib.reload(gmft.pdf_bindings.bindings_pdfium)
importlib.reload(gmft.pdf_bindings)
from gmft.pdf_bindings import PyPDFium2Document
from gmft import CroppedTable, TableDetector

from gmft import AutoTableFormatter
from IPython.display import display
from gmft import AutoFormatConfig

import pandas as pd
from gmft.table_function import TATRFormatConfig
detector = TableDetector()

from IPython.display import display
import pandas as pd

def ingest_pdf(source_path):
    doc = PyPDFium2Document(source_path)
    tables = []
    for page in doc:
        tables += detector.extract(page)
    
    
    filtered_tables = [item for item in tables if item.confidence_score < 1]
    
    for i in range(len(filtered_tables)):
        formatter = AutoTableFormatter()
        formatter.config = AutoFormatConfig()
        ft = formatter.extract(filtered_tables[i])
        
        # Display the image of the table
        display(ft.image())
        
        
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            display(ft.df().fillna(""))
        ft.outliers
        # Visualize the table
        ft.visualize()
        ft.captions()
        
      
        df = ft.df()
        df.to_csv(f"table_{i}.csv")
        display(df)
# ingest_pdf("pdf_path")