from typing import Optional, List

from .adf_content_node import ADFContentObject
from .adf_object import ADFObject

ADFTableCell = ADFContentObject.node_class_factory('tableCell')
ADFTableHeader = ADFContentObject.node_class_factory('tableHeader')


class ADFTable(ADFContentObject.node_class_factory('table')):
    def __init__(self, chain_mode=True, **kwargs):
        super(ADFTable, self).__init__(chain_mode=chain_mode, **kwargs)

    @classmethod
    def create(cls,
               dimension: Optional[List[int]] = None,
               spanned_layout: Optional[List[List[int]]] = None,
               with_header=False):
        if (dimension is None and spanned_layout is None) or (dimension is not None and spanned_layout is not None):
            raise RuntimeError('Specify one and only one of the dimension and spanned_layout.')
        if isinstance(dimension, int):
            dimension = (dimension, 1)

        table = cls()
        if dimension is not None:
            col, row = dimension
            rows = [
                ADFTableRow.create(col, is_header=with_header and i == 0)
                for i in range(row)
            ]
        else:
            rows = [
                ADFTableRow.create(spanned_layout=row_span, is_header=with_header and i == 0)
                for i, row_span in enumerate(spanned_layout)
            ]
        table.extend_content(rows)
        return table

    def append_row(self, spanned_layout: Optional[List[int]] = None):
        if spanned_layout is None:
            new_row = ADFTableRow.create(dimension=self._max_width)
        else:
            new_row = ADFTableRow.create(spanned_layout=spanned_layout)
        self.extend_content(new_row)
        return new_row

    def extend_content(self, rows):
        if isinstance(rows, ADFObject):
            rows = [rows]
        if any(row.type != 'tableRow' for row in rows):
            raise RuntimeError(f'ADFTable only accepts tableRow as child node. {rows=}')

        if any(
                sum((cell.local_info['attrs']['colspan'] for cell in row), 0) > self._max_width for row in rows
        ) and self._max_width != 0:
            raise ValueError('Input Row is wider than the existing table.')

        return super(ADFTable, self).extend_content(rows)

    @property
    def _max_width(self):
        return max(
            (sum((cell.local_info['attrs']['colspan'] for cell in row), 0) for row in self),
            default=0
        )


class ADFTableRow(ADFContentObject.node_class_factory('tableRow')):
    @classmethod
    def create(cls,
               dimension: Optional[int] = None,
               spanned_layout: Optional[List[int]] = None,
               is_header=False):
        if (dimension is None and spanned_layout is None) or (dimension is not None and spanned_layout is not None):
            raise RuntimeError('Specify one and only one of the dimension and spanned_layout.')
        new_cell_class = ADFTableHeader if is_header else ADFTableCell
        new_row = cls()

        if dimension is not None:
            spanned_layout = [1] * dimension
        attrs_list = [{'colspan': span} for span in spanned_layout]
        cells = [new_cell_class(attrs=attrs) for attrs in attrs_list]
        new_row.extend_content(cells)
        return new_row

    def extend_content(self, cells):
        if isinstance(cells, ADFObject):
            cells = [cells]
        if any(cell.type not in ('tableCell', 'tableHeader') for cell in cells):
            raise RuntimeError(f'ADFTableRow only accept child type of "tableCell"or "tableHeader"')

        return super(ADFTableRow, self).extend_content(cells)
