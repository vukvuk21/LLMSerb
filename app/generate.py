from fpdf import FPDF
import os

output_dir = "data"
os.makedirs(output_dir, exist_ok=True)

# PDF content: (filename, title, content)
pdfs = [
    ("anatomija.pdf", "Anatomija",
     "Mozak kontrolise mnoge funkcije tela ukljucujuci govor, pokret i memoriju.\n"
     "Cerebellum je deo mozga koji pomaze u koordinaciji i ravnotezi.\n"
     "Kostur se sastoji od preko 200 kostiju koje daju strukturu i zastitu."),

    ("farmakologija.pdf", "Farmakologija",
     "Paracetamol se koristi za bol i temperaturu.\n"
     "Antibiotici deluju protiv bakterija, ali ne protiv virusa.\n"
     "Insulin regulise nivo secera u krvi i koristi se kod dijabetesa."),

    ("fiziologija.pdf", "Fiziologija",
     "Disajni sistem ukljucuje nos, dusnik, bronhije i pluca.\n"
     "Jetra igra vaznu ulogu u detoksikaciji organizma.\n"
     "Krv prenosi kiseonik i hranljive materije kroz telo."),

    ("lekovi_za_temperaturu.pdf", "Lekovi za temperaturu",
     "Paracetamol i ibuprofen su najcesce korisceni lekovi za snizavanje telesne temperature.\n"
     "Paracetamol deluje centralno, dok ibuprofen ima i antiinflamatorno dejstvo."),

    ("mozganatomija.pdf", "Mozgova anatomija",
     "Cerebellum se nalazi u zadnjem delu mozga i odgovoran je za ravnotezu.\n"
     "Mozdano stablo povezuje mozak sa kicmenom mozdinom i regulise disanje."),

    ("metabolizam.pdf", "Metabolizam",
     "Jetra razlaze toksine i lekove, ucestvujuci u metabolizmu.\n"
     "Krv prenosi produkte metabolizma do bubrega gde se izlucuju."),
]

for filename, title, content in pdfs:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=title, ln=True, align='C')
    pdf.ln(10)
    for line in content.split("\n"):
        pdf.multi_cell(0, 10, line)
    pdf.output(os.path.join(output_dir, filename))

print(f"Generisano {len(pdfs)} PDF-ova u '{output_dir}' direktorijumu.")
