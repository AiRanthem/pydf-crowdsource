import os.path
import time

from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


def create_watermark(content: str, path: str):
    """水印信息"""
    # 默认大小为21cm*29.7cm
    file_name = os.path.abspath(path)
    c = canvas.Canvas(file_name, pagesize=(30 * cm, 30 * cm))
    # 移动坐标原点(坐标系左下为(0,0))
    c.translate(10 * cm, 5 * cm)

    # 设置字体
    c.setFont("Helvetica", 14)
    # 指定描边的颜色
    c.setStrokeColorRGB(0, 1, 0)
    # 指定填充颜色
    c.setFillColorRGB(0, 1, 0)
    # 旋转45度,坐标系被旋转
    c.rotate(30)
    # 指定填充颜色
    c.setFillColorRGB(0, 0, 0, 0.1)
    # 设置透明度,1为不透明
    # c.setFillAlpha(0.1)
    # 画几个文本,注意坐标系旋转的影响
    for i in range(5):
        for j in range(10):
            a = 10 * (i - 1)
            b = 5 * (j - 2)
            c.drawString(a * cm, b * cm, content)
            c.setFillAlpha(0.1)
    # 关闭并保存pdf文件
    c.save()
    return file_name


def add_watermark(pdf_file_in, pdf_file_mark, pdf_file_out):
    """把水印添加到pdf中"""
    pdf_output = PdfFileWriter()
    input_stream = open(pdf_file_in, 'rb')
    pdf_input = PdfFileReader(input_stream, strict=False)

    # 获取PDF文件的页数
    page_num = pdf_input.getNumPages()

    # 读入水印pdf文件
    with open(pdf_file_mark, 'rb') as f:
        pdf_watermark = PdfFileReader(f, strict=False)
        # 给每一页打水印
        for i in range(page_num):
            page = pdf_input.getPage(i)
            page.mergePage(pdf_watermark.getPage(0))
            page.compressContentStreams()  # 压缩内容
            pdf_output.addPage(page)
        pdf_output.write(open(pdf_file_out, 'wb'))

    input_stream.close()


def merge(files: list, out_dir: str) -> str:
    """
    merge given pdf files
    :param files: pdf file paths
    :param out_dir: output dir for merged file
    :return: the absulote path of merged file
    """
    merger = PdfFileMerger()
    for f in files:
        merger.append(f)
    out_file = os.path.join(out_dir, f"{time.time()}.pdf")
    merger.write(out_file)
    merger.close()
    return out_file
