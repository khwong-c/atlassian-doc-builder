from typing import Optional, List

from .adf_content_node import ADFContentObject


class ADFTable(ADFContentObject.node_class_factory('table')):
    @classmethod
    def create(cls,
               dimension: Optional[List[int]] = None,
               spanned_layout: Optional[List[List[int]]] = None,
               with_header=False):
        ...

    def append_row(self, spanned_layout: Optional[List[int]] = None):
        ...


class ADFTableRow(ADFContentObject.node_class_factory('tableRow')):
    @classmethod
    def create(cls,
               dimension: Optional[int] = None,
               spanned_layout: Optional[List[int]] = None,
               is_header=False):
        ...


ADFTableCell = ADFContentObject.node_class_factory('tableCell')
ADFTableHeader = ADFContentObject.node_class_factory('tableHeader')
