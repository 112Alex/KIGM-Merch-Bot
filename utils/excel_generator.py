import io
from openpyxl import Workbook

async def generate_bought_goods_excel(data: list) -> io.BytesIO:
    """Generates an Excel file for bought goods from a list of data and returns it as BytesIO."""
    workbook = Workbook()
    ws = workbook.active
    ws.title = "Bought Goods"

    # Add header row
    ws.append(['tg-id', 'название товара', 'имя', 'фамилия', 'группа', 'возраст'])

    # Add data rows
    for row in data:
        ws.append(row)

    # Save the workbook to a BytesIO object
    excel_file = io.BytesIO()
    workbook.save(excel_file)
    excel_file.seek(0)  # Rewind to the beginning of the stream
    return excel_file
