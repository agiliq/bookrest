from django.db import connections, models

from collections import OrderedDict

class ConnectionToModels:
    """
    Given a connection,
    Reurn a list of Django tables
    """

    def __init__(self, connection):
        self.connection = connection

    def get_model(self, table_name):
        table_fields = self.get_fields(table_name)
        model_fields = [self.get_field(table_name, field_info)
            for field_info in table_fields]
        attrs = dict(model_fields)
        attrs['__module__'] = 'bookrest.models'
        Model = type(table_name.upper(), (models.Model,), attrs)
        return Model

    def get_tables(self):
        """
        Get a list of tables in the DB
        """
        with self.connection.cursor() as cursor:
            table_info = self.connection.introspection.get_table_list(cursor)
        return table_info

    def get_fields(self, table_name):
        """
        get a list of fields in a table
        """
        with self.connection.cursor() as cursor:
            return self.connection.introspection.get_table_description(cursor, table_name)

    def get_field(self, table_name, field_info):
        """
        Given the database connection, the table name, and the cursor field_info
        description, this routine will return the given field type name, as
        well as any additional keyword parameters and notes for the field.
        """
        field_params = OrderedDict()
        field_notes = []

        try:
            field_type = self.connection.introspection.get_field_type(field_info[1], field_info)
        except KeyError:
            field_type = 'TextField'
            field_notes.append('This field type is a guess.')

        # This is a hook for data_types_reverse to return a tuple of
        # (field_type, field_params_dict).
        if type(field_type) is tuple:
            field_type, new_params = field_type
            field_params.update(new_params)

        # Add max_length for all CharFields.
        if field_type == 'CharField' and field_info[3]:
            field_params['max_length'] = int(field_info[3])

        if field_type == 'DecimalField':
            if field_info[4] is None or field_info[5] is None:
                field_notes.append(
                    'max_digits and decimal_places have been guessed, as this '
                    'database handles decimal fields as float')
                field_params['max_digits'] = field_info[4] if field_info[4] is not None else 10
                field_params['decimal_places'] = field_info[5] if field_info[5] is not None else 5
            else:
                field_params['max_digits'] = field_info[4]
                field_params['decimal_places'] = field_info[5]
        return field_info.name, getattr(models, field_type)(**field_params)

