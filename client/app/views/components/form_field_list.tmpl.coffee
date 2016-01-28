{table, thead, tfoot, tbody, tr, th, td, a, i} = require('../../modules/tags')
c = require('../../modules/content').get
{ucfirst} = require('../../modules/auxiliaries')
formFieldInput = require('./form_field_input.tmpl')
formFieldSelect = require('./form_field_select.tmpl')
icon = require('./icon.tmpl')


field = ({name, index, col, row, lock}) ->
    return row[col.name] if lock

    return formFieldSelect({
        name: "#{name}.#{index}.#{col.name}"
        value: row[col.name]
        options: col.options
    }) if col.type is 'select'

    return formFieldInput({
        type: 'text'
        size: 10
        name: "#{name}.#{index}.#{col.name}"
        value: row[col.name]
        # TODO-3 placeholder
        # TODO-3 default
    }) if col.type is 'text'

module.exports = (data) ->
    ###
    data.columns: array of field names
    data.values: array of objects
    data.lock [Boolean]
    data.name
    ###

    value = if data.value and data.value.length
        data.value
    else
        [{}]

    columns = data.columns or []

    return table(
        {attributes: {'data-name': data.name}}
        thead(
            tr(
                th(
                    {attributes: {'data-col': col.name}}
                    ucfirst(col.name)
                ) for col in columns
                # TODO-2 th()  # For reordering
                th()  # For deleting
            )
        )
        tfoot(
            tr(
                td(
                    {colSpan: columns.length + 1}  # TODO-2 +2 reordering
                    a(
                        {href: '#', className: 'form-field--list__add-row'}
                        icon('create')
                        ' Add Row'
                    )
                )
            )
        )
        tbody(
            tr(
                td(
                    field({
                        name: data.name
                        index
                        col
                        row
                        lock: data.lock
                    })
                ) for col in columns
                # TODO-2 move row td(
                #     a(
                #         {title: 'Reorder', href: '#', className: 'move-row'}
                #         icon('move')
                #     )
                # )
                td(
                    a(
                        {
                            title: 'Remove'
                            href: '#'
                            className: 'form-field--list__remove-row'
                            attributes: {
                                'data-index': index
                            }
                        }
                        icon('remove')
                    )
                )
            ) for row, index in value
        )
    )
