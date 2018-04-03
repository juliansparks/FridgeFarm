from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms_components import DateField
from wtforms.validators import ValidationError, DataRequired, Optional


class CreateFridgeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], default='Name')
    description = StringField('Description', default='Description')
    submit = SubmitField('Create')

    def validate_name(self, name: str) -> None:
        if name is 'Name':
            raise ValidationError('Please use a different username.')

    def validate_description(self, description: str) -> None:
        if description is 'Description':
            raise ValidationError('Please use a different username.')


class CreateItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], default='')
    description = StringField('Description', default='')
    quantity = IntegerField('Quantity', default=1)
    experation = DateField('Expiration', validators=[Optional()])
    submit = SubmitField('Create')
