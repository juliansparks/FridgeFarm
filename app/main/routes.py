from flask import render_template, flash, redirect, url_for, abort
from app import db
from flask_classful import FlaskView, route
from app.main import register_view
from flask_login import current_user, login_required
from app.main.forms import CreateFridgeForm, CreateItemForm
from app.models import Fridge, Item


@register_view
class HomepageView(FlaskView):
    """ View for the homepage. """

    route_base = ''

    @login_required
    def index(self) -> str:
        """ The Homepage """
        return render_template('index.html', title='Home Page')


@register_view
class FridgeView(FlaskView):
    """ View for fridges. """

    decorators = [login_required]

    @route('/', methods=['GET', 'POST'])
    def all_fridges(self) -> str:
        """ Renders a list of all the users's fridges
        and includes form to create a new fridge. """
        user = current_user
        form = CreateFridgeForm()
        if form.validate_on_submit():
            fridge = Fridge(
                name=form.name.data,
                description=form.description.data,
                user_id=current_user.id)
            db.session.add(fridge)
            db.session.commit()
            flash(f'Fridge {fridge.name} created!')
            return redirect(url_for('main.FridgeView:all_fridges'))
        return render_template(
            'user.html', title='Create a new Fridge', user=user, form=form)

    def get_fridge(self, fridge_id: str) -> str:
        """ Renders a view of a fridge and the items it contains. """
        fridge = Fridge.by_id(fridge_id)
        return render_template('fridge.html', title=fridge.name, fridge=fridge)

    def remove_fridge(self, fridge_id: str) -> str:
        """ Deletes a fridge. """
        Fridge.by_id(fridge_id).remove()
        return redirect(url_for('main.FridgeView:all_fridges'))

    @route('create_item/<fridge_id>', methods=['GET', 'POST'])
    def create_item(self, fridge_id: str) -> str:
        """ Creates a new items and adds it to the specified fridge. """
        # fridge = Fridge.query.filter_by(id=fridge_id).first_or_404()
        fridge = Fridge.by_id(fridge_id)
        form = CreateItemForm()
        if form.validate_on_submit():
            item = fridge.add_item(
                name=form.name.data,
                description=form.description.data,
                quantity=form.quantity.data,
                expiration=form.experation.data)
            flash(f'{item.name} added to {fridge.name}!')
            return redirect(
                url_for('main.FridgeView:get_fridge', fridge_id=fridge.id))
        return render_template(
            'createitem.html', title='Add an Item', form=form)

    def remove_item(self, fridge_id: str, item_id: str) -> str:
        """ Delete the specified item from the specified fridge. """
        fridge = Fridge.by_id(fridge_id)
        item = Item.by_id(item_id)
        if item not in fridge:
            abort(404)
        item.remove()
        return redirect(
            url_for('main.FridgeView:get_fridge', fridge_id=fridge.id))
