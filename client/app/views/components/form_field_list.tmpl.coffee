{table, thead, tbody, tr, th, td, a, i} = require('../../modules/tags')
c = require('../../modules/content').get
{ucfirst} = require('../../modules/auxiliaries')
formFieldInput = require('./form_field_input.tmpl')

module.exports = (data) ->
    ###
    data.columns: array of field names
    data.values: array of objects
    data.lock [Boolean]
    data.name
    ###

    values = if data.values and data.values.length
        data.values
    else
        [{}]

    columns = data.columns or []

    return table(
        thead(
            tr(
                th(ucfirst(col)) for col in columns
                # TODO th()  # For reordering
                th()  # For deleting
            )
        )
        tbody(
            tr(
                td(
                    # TODO@ allow select/boolean
                    #       for `correct` and `kind` columns
                    formFieldInput({
                        type: 'text'
                        size: 10
                        name: "#{data.name}.#{index}.#{col}"
                        value: row[col]
                        # TODO placeholder
                        # TODO default
                    }) if not data.lock
                    row[col] if data.lock
                ) for col, index in columns
                # TODO move row td(
                #     a(
                #         {title: 'Reorder', href: '#', className: 'move-row'}
                #         i({className: 'fa fa-arrows-v'})
                #     )
                # )
                td(
                    a(
                        {title: 'Remove', href: '#', className: 'remove-row'}
                        i({className: 'fa fa-times-circle'})
                    )
                )
            ) for row in values
            tr(
                {className: 'add-row-tr'}
                td(
                    {colSpan: columns.length + 1}
                    a(
                        {href: '#', className: 'add-row'}
                        i({className: 'fa fa-plus'})
                        ' Add Row'
                    )
                )
            )
        )
    )
