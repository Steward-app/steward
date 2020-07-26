from absl import logging
from flask import Blueprint, render_template, flash, redirect, request
from flask_login import login_required, current_user

import grpc
from steward import registry_pb2_grpc
from steward import maintenance_pb2 as m
from steward import asset_pb2 as a

from app.forms import MaintenanceForm

bp = Blueprint("maintenance", __name__)

logging.set_verbosity(logging.INFO)

channel = grpc.insecure_channel('localhost:50051')
maintenances = registry_pb2_grpc.MaintenanceServiceStub(channel)
assets = registry_pb2_grpc.AssetServiceStub(channel)

@bp.route('/maintenances')
@login_required
def list_maintenances():
    return render_template('maintenances.html', maintenances=maintenances.ListMaintenances(m.ListMaintenancesRequest()))

@bp.route('/maintenance/create', methods=['GET', 'POST'])
@login_required
def maintenance_create():
    form = MaintenanceForm()
    form.asset.choices = [(a._id, a.name) for a in get_available_assets(current_user.user.organization_id)]
    form.schedule.choices = [(a._id, a.name) for a in get_available_assets(current_user.user.organization_id)]
    if form.validate_on_submit():
        return maintenance_submit(form)
    return render_template('maintenance_edit.html', form=form, view="Create Maintenance")

@bp.route('/maintenance/<maintenance_id>')
@login_required
def maintenance(maintenance_id=None):
    return render_template('maintenance.html', maintenance=maintenances.GetMaintenance(m.GetMaintenanceRequest(_id=maintenance_id)))

@bp.route('/maintenance/edit/<maintenance_id>', methods=['GET', 'POST'])
@login_required
def maintenance_edit(maintenance_id=None):
    form = MaintenanceForm()

    if form.validate_on_submit():
        return maintenance_submit(form, maintenance_id)
    else:
        logging.info('loading current values because: {}'.format(form.errors))
        old_maintenance = maintenances.GetMaintenance(m.GetMaintenanceRequest(_id=maintenance_id))
        form = MaintenanceForm(obj=old_maintenance)
        form.asset.choices = [(a._id, a.name) for a in get_available_assets(current_user.user.organization_id)]
        form.schedule.choices = [(a._id, a.name) for a in get_available_assets(current_user.user.organization_id)]

    return render_template('maintenance_edit.html', form=form, view='Edit Maintenance')

def maintenance_submit(form, maintenance_id=None):
    maintenance = m.Maintenance()
    maintenance.name = form.name.data
    maintenance.description = form.description.data
    maintenance.enabled = form.enabled.data
    maintenance.asset.name = form.asset.data
    maintenance.schedule.description = form.schedule.data

    if maintenance_id:
        new_maintenance = maintenances.UpdateMaintenance(
                m.UpdateMaintenanceRequest(_id=maintenance_id, maintenance=maintenance)
                )
    else:
        new_maintenance = maintenances.CreateMaintenance(maintenance)
    return redirect('/maintenance/{}'.format(new_maintenance._id))

def get_available_assets(organization_id):
    return assets.ListAssets(a.ListAssetsRequest(organization_id=organization_id))
