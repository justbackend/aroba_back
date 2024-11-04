from rest_framework import serializers


def create_serializer(fields: dict) -> type(serializers.Serializer):
    field_mapping = {
        int: serializers.IntegerField,
        str: serializers.CharField,
        bool: serializers.BooleanField,
        float: serializers.FloatField,
    }

    serializer_fields = {}
    for field_name, field_type in fields.items():
        serializer_field = field_mapping.get(field_type)
        if not serializer_field:
            raise TypeError(f"Unsupported field type: {field_type}")
        serializer_fields[field_name] = serializer_field()

    return type("DynamicSerializer", (serializers.Serializer,), serializer_fields)
