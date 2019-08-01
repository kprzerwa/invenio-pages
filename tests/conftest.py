# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Pytest configuration."""

from __future__ import absolute_import, print_function

import pytest
from flask import Flask
from invenio_admin import InvenioAdmin
from invenio_db import InvenioDB, db

from invenio_pages import InvenioPages, Page


@pytest.fixture
def app(request):
    """Flask application fixture."""
    app = Flask('testapp')
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI='sqlite://',
    )
    InvenioDB(app)
    with app.app_context():
        db.create_all()

    def teardown():
        with app.app_context():
            db.drop_all()

    request.addfinalizer(teardown)
    return app


@pytest.fixture
def admin_fixture(pages_fixture):
    """Admin fixture."""
    def unprotected_factory(base_class):

        class UnprotectedAdminView(base_class):

            def is_accesible(self):
                return True

            def inaccessible_callback(self, name, **kwargs):
                pass

        return UnprotectedAdminView

    InvenioAdmin(
        pages_fixture,
        view_class_factory=unprotected_factory,
    )

    return pages_fixture


@pytest.fixture
def pages_fixture(app):
    """Page fixtures."""
    InvenioPages(app)
    with app.app_context():
        pages = [
            Page(
                url='/dogs',
                title='Page for Dogs!',
                content='Generic dog.',
                template_name='invenio_pages/default.html',
            ),
            Page(
                url='/dogs/shiba',
                title='Page for doge!',
                content='so doge!',
                template_name='invenio_pages/default.html',
            ),
            Page(
                url='/cows/',
                title='Page for Cows!',
                content='Generic cow.',
                template_name='invenio_pages/default.html',
            ),
        ]
        for page in pages:
            db.session.add(page)
        db.session.commit()

    return app
