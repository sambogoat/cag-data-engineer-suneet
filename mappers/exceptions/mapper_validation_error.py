class MapperValidationError(Exception):

    def __init__(self, message="Error applying mapper validation", schema_path=None, validation_details=None):
        self.message = message
        self.schema_path = schema_path
        self.validation_details = validation_details
        super().__init__(self.message)

    def __str__(self):
        if self.schema_path and self.validation_details:
            return f'{self.message}, schema: {self.schema_path}\n{self.validation_details}'
        else:
            return self.message
