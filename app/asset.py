from absl import logging
from flask import Blueprint, render_template, flash, redirect, request
from flask_login import login_required

import grpc
from steward import registry_pb2_grpc
from steward import asset_pb2 as a

from app.forms import AssetForm

bp = Blueprint("asset", __name__)

logging.set_verbosity(logging.INFO)

channel = grpc.insecure_channel('localhost:50051')
assets = registry_pb2_grpc.AssetServiceStub(channel)

@bp.route('/assets')
@login_required
def list_assets():
    return render_template('assets.html', assets=assets.ListAssets(a.ListAssetsRequest()))

@bp.route('/asset/create', methods=['GET', 'POST'])
@login_required
def asset_create():
    form = AssetForm()
    if form.validate_on_submit():
        asset = a.Asset()
        asset.name = form.name.data
        asset.description = form.description.data
        new_asset = assets.CreateAsset(asset)
        flash('Asset \'{}\' Created!'.format(form.name.data))
        return redirect('/asset/{}'.format(new_asset._id))
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
        logging.error('edit form checks out, pushing updates')
        asset = a.Asset()
        asset.name = form.name.data
        asset.description = form.description.data
        asset.enabled = form.enabled.data
        asset.asset.name = form.asset.data
        asset.schedule.description = form.schedule.data

        new_asset = assets.UpdateAsset(a.UpdateAssetRequest(_id=asset_id, asset=asset))
        flash('Asset \'{}\' Updated!'.format(form.name.data))
        return redirect('/asset/{}'.format(new_asset._id))
    else:
        logging.info('loading current values because: {}'.format(form.errors))
        old_asset = assets.GetAsset(a.GetAssetRequest(_id=asset_id))
        form = AssetForm(obj=old_asset)

    return render_template('asset_edit.html', form=form, view='Edit Asset')
