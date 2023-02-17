import pytest

from atlassian_doc_builder import ADFTable


class TestADFTable:
    def test_create_table_no_input(self):
        with pytest.raises(RuntimeError):
            ADFTable.create()

    def test_create_with_dimension(self):
        cols, rows = 4, 5
        table = ADFTable.create([cols, rows])
        table_row = len(table)
        assert table_row == rows
        assert all(len(row) == cols for row in table)

    def test_create_with_single_dimension(self):
        cols, rows = 4, 1
        table = ADFTable.create(cols)
        assert len(table) == rows
        assert len(table[0]) == cols

    def test_create_with_spanned_layout(self):
        layout = [
            [1] * 6,
            [2, 3, 1],
            [3, 3],
        ]
        table = ADFTable.create(spanned_layout=layout)
        assert len(table) == len(layout)
        assert all(len(row_table) == len(row_input) for row_table, row_input in zip(table, layout))
        assert all(all(
            row_cell.local_info['attrs']['colspan'] == span_size
            for row_cell, span_size in zip(row_table, row_input)
        ) for row_table, row_input in zip(table, layout))

    def test_create_table_mixed_not_allowed(self):
        cols, rows = 4, 5
        input_layout = [
            [1] * 4,
        ]
        with pytest.raises(RuntimeError):
            ADFTable.create(dimension=[cols, rows], spanned_layout=input_layout)

    def test_create_table_with_header(self):
        table = ADFTable.create([4, 5], with_header=True)
        assert all(cell.type == 'tableHeader' for cell in table[0])
        assert all(cell.type == 'tableCell'
                   for i, row in enumerate(table)
                   for cell in row
                   if i > 0
                   )

    def test_append_row_empty_table(self):
        table = ADFTable()
        new_row = table.append_row()
        assert new_row is table[-1]
        assert len(new_row) == 0

    def test_append_row_regular_layout(self):
        cols, rows = 4, 5
        table = ADFTable.create([cols, rows])
        new_row = table.append_row()
        assert new_row is table[-1]
        assert len(table) == rows + 1
        assert len(new_row) == cols

    def test_append_row_spanned_layout(self):
        layout = [
            [1] * 6,
            [2, 3, 2],
            [3, 3],
        ]
        table = ADFTable.create(spanned_layout=layout)
        new_row = table.append_row()
        assert new_row is table[-1]
        assert len(table) == len(layout) + 1
        assert len(new_row) == max(sum(row_layout) for row_layout in layout)
        assert all(cell.local_info['attrs']['colspan'] == 1 for cell in new_row)

    def test_append_row_spanned_row(self):
        cols, rows = 4, 5
        new_row_layout = [2, 2]
        table = ADFTable.create([cols, rows])
        new_row = table.append_row(new_row_layout)
        assert new_row is table[-1]
        assert len(table) == rows + 1
        assert len(new_row) == len(new_row_layout)
        assert all(cell.local_info['attrs']['colspan'] == new_row_span
                   for cell, new_row_span in zip(new_row, new_row_layout)
                   )

    def test_append_row_oversize_not_allowed(self):
        cols, rows = 4, 5
        table = ADFTable.create([cols, rows])
        with pytest.raises(ValueError):
            table.append_row([1] * (cols + 10))
