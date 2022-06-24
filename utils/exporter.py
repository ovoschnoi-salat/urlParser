from scrapy.exporters import JsonLinesItemExporter
from scrapy.utils.python import to_bytes
from utils.utils import link_key, hints_key


class TxtItemExporter(JsonLinesItemExporter):
    def export_item(self, item):
        if hints_key in item:
            self.file.write(to_bytes("HINTS:\n", self.encoding))
            for hint in item[hints_key]:
                self.file.write(to_bytes(hint + "\n", self.encoding))
            self.file.write(to_bytes("\n", self.encoding))
        if link_key in item:
            self.file.write(to_bytes(item[link_key] + "\n", self.encoding))
