from absl import logging

from datetime import datetime, date
import calendar
from google.protobuf.json_format import MessageToDict
from collections import namedtuple

from flask import Blueprint, render_template, flash, redirect, request
from flask_login import login_required

import grpc
from steward import registry_pb2_grpc
from steward import asset_pb2 as a

from app.forms import AssetForm, DeleteForm
from app import channels

bp = Blueprint("asset", __name__)

logging.set_verbosity(logging.INFO)

channel = grpc.insecure_channel(channels.ASSET_ENDPOINT)
assets = registry_pb2_grpc.AssetServiceStub(channel)

@bp.route('/assets')
@login_required
def asset_list():
    return render_template('assets.html', assets=assets.ListAssets(a.ListAssetsRequest()))

@bp.route('/asset/create', methods=['GET', 'POST'])
@login_required
def asset_create():
    form = AssetForm()
    if form.validate_on_submit():
        return asset_submit(form)
    return render_template('asset_edit.html', form=form, view="Create Asset")

@bp.route('/asset/<asset_id>')
@login_required
def asset(asset_id=None):
    return render_template('asset.html', asset=assets.GetAsset(a.GetAssetRequest(_id=asset_id)))

@bp.route('/asset/edit/<asset_id>', methods=['GET', 'POST'])
@login_required
def asset_edit(asset_id=None):
    form = AssetForm()

    if form.validate_on_submit():
        return asset_submit(form, asset_id)
    else:
        logging.info('loading current values because: {}'.format(form.errors))
        
        old_asset = assets.GetAsset(a.GetAssetRequest(_id=asset_id))

        # All of this fuckery is needed because the proto object validates field types,
        # so we can't just change the field to a datetime object but need a new object
        asset_dict = MessageToDict(message=old_asset, preserving_proto_field_name=True)
        asset_dict['acquired'] = date.fromtimestamp(old_asset.acquired)
        # Have to delete _id since it's not a valid field for a namedtuple
        del asset_dict['_id']
        asset_obj = namedtuple("Asset", asset_dict.keys()) (*asset_dict.values())
        form = AssetForm(obj=asset_obj)

    return render_template('asset_edit.html', form=form, view='Edit Asset')

@bp.route('/asset/delete/<asset_id>', methods=['GET', 'POST'])
@login_required
def asset_delete(asset_id=None):
    form = DeleteForm()
    asset = assets.GetAsset(a.GetAssetRequest(_id=asset_id))

    if form.validate_on_submit():
        deleted = assets.DeleteAsset(a.DeleteAssetRequest(_id=asset_id))
        if deleted and deleted.name and not deleted._id:
            flash('Asset deleted: {}'.format(deleted.name))
            return redirect('/assets')
        else:
            flash('Failed to delete asset: {}'.format(deleted))
            logging.error('Failed to delete asset: {}'.format(deleted))
            asset = 'error'
            return render_template('delete.html', form=form, view='delete', obj_type='Asset', obj=None, name='deleted?')
    return render_template('delete.html', form=form, view='delete', obj_type='Asset', obj=asset, name=asset.name)


def asset_submit(form, asset_id=None):
        asset = a.Asset()
        asset.name = form.name.data
        asset.description = form.description.data
        ts = calendar.timegm(form.acquired.data.timetuple())
        asset.acquired = ts

        if asset_id:
            new_asset = assets.UpdateAsset(a.UpdateAssetRequest(_id=asset_id, asset=asset))
        else:
            new_asset = assets.CreateAsset(asset)
        return redirect('/asset/{}'.format(new_asset._id))

