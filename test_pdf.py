from fpdf import FPDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("helvetica", size=12)
pdf.cell(text="Hello World")
out = pdf.output()
print(type(out))
