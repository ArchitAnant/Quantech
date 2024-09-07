import ocrmypdf

def convert_to_machine_readable(input_pdf, output_pdf):
    """Convert a non-machine-readable PDF to a machine-readable PDF."""
    ocrmypdf.ocr(input_pdf, output_pdf)

convert_to_machine_readable("non_machine_readable.pdf", "output.pdf")