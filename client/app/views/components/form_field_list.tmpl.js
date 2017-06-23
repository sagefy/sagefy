const { table, thead, tfoot, tbody, tr, th, td, a } =
    require('../../modules/tags')
const { ucfirst } = require('../../modules/auxiliaries')
const formFieldInput = require('./form_field_input.tmpl')
const formFieldSelect = require('./form_field_select.tmpl')
const icon = require('./icon.tmpl')

const field = ({ name, index, col, row, lock }) => {
    if (lock) { return row[col.name] }

    if (col.type === 'select') {
        return formFieldSelect({
            name: `${name}.${index}.${col.name}`,
            value: row[col.name],
            options: col.options,
        })
    }

    if (col.type === 'text') {
        return formFieldInput({
            type: 'text',
            size: 30,
            name: `${name}.${index}.${col.name}`,
            value: row[col.name],
            // TODO-3 placeholder
            // TODO-3 default
        })
    }
}

module.exports = (data) => {
    /*
    data.columns: array of field names
    data.values: array of objects
    data.lock [Boolean]
    data.name
    */

    let value
    if (data.value && data.value.length) {
        value = data.value
    } else {
        value = [{}]
    }

    const columns = data.columns || []

    return table(
        { attributes: { 'data-name': data.name } },
        thead(
            tr(
                columns.map(col => th(
                    { attributes: { 'data-col': col.name } },
                    ucfirst(col.name)
                )),
                // TODO-2 th()  // For reordering
                th()  // For deleting
            )
        ),
        tfoot(
            tr(
                td(
                    { colSpan: columns.length + 1 },  // TODO-2 +2 reordering
                    a(
                        { href: '#', className: 'form-field--list__add-row' },
                        icon('create'),
                        ' Add Row'
                    )
                )
            )
        ),
        tbody(
            value.map((row, index) => tr(
                columns.map(col => td(
                    field({
                        name: data.name,
                        index,
                        col,
                        row,
                        lock: data.lock,
                    })
                )),
                // TODO-2 move row td(
                //     a(
                //         {title: 'Reorder', href: '#', className: 'move-row'}
                //         icon('move')
                //     )
                // )
                td(
                    a(
                        {
                            title: 'Remove',
                            href: '#',
                            className: 'form-field--list__remove-row',
                            attributes: {
                                'data-index': index,
                            },
                        },
                        icon('remove')
                    )
                )
            ))
        )
    )
}
