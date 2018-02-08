# This file is part of Invenio.
# Copyright (C) 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014 CERN.
#
# Invenio is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

__lastupdated__ = """$Date$"""

__revision__ = "$Id$"

import os
import errno
import time
import cgi
import sys
import shutil

from urllib import urlencode
from collections import defaultdict

from invenio.config import \
     CFG_ACCESS_CONTROL_LEVEL_SITE, \
     CFG_SITE_LANG, \
     CFG_SITE_NAME, \
     CFG_SITE_URL, \
     CFG_SITE_SECURE_URL, \
     CFG_WEBSUBMIT_STORAGEDIR, \
     CFG_PREFIX, \
     CFG_CERN_SITE
from invenio import webinterface_handler_config as apache
from invenio.dbquery import run_sql
from invenio.access_control_engine import acc_authorize_action
from invenio.access_control_admin import acc_is_role
from invenio.webpage import warning_page, page
from invenio.webuser import getUid, page_not_authorized, collect_user_info, \
                            isGuestUser
from invenio.webinterface_handler import wash_urlargd, WebInterfaceDirectory
from invenio.urlutils import make_canonical_urlargd, redirect_to_url
from invenio.messages import gettext_set_language
from invenio.errorlib import register_exception
from invenio.htmlutils import is_html_text_editor_installed
import invenio.template
#websubmit_templates = invenio.template.load('websubmit')
from invenio.session import get_session
from invenio.jsonutils import json, CFG_JSON_AVAILABLE
import invenio.template
webstyle_templates = invenio.template.load('webstyle')
websearch_templates = invenio.template.load('websearch')

class WebInterfaceGalterPages(WebInterfaceDirectory):

    _exports = ['test']

    def index(self, req, form):

        args = wash_urlargd(form, {
            'c': (str, CFG_SITE_NAME),
            'doctype': (str, ''),
            'act': (str, ''),
            'startPg': (str, "1"),
            'access': (str, ''),
            'mainmenu': (str, ''),
            'fromdir': (str, ''),
            'nextPg': (str, ''),
            'nbPg': (str, ''),
            'curpage': (str, '1'),
            'step': (str, '0'),
            'mode': (str, 'U'),
            })

        args["doctype"] = args["doctype"].strip()
        args["act"] = args["act"].strip()

        def _index(req, c, ln, doctype, act, startPg, access,
                   mainmenu, fromdir, nextPg, nbPg, curpage, step,
                   mode):
            uid = getUid(req)

            if uid == -1 or CFG_ACCESS_CONTROL_LEVEL_SITE >= 1:
                return page_not_authorized(req, "direct",
                                            navmenuid='submit')

            if doctype == "":
                return page(title=('Galter'),
                  body="<h1>Hello Galter</h1>",
                  description="galter desc",
                  keywords="galter-key",
                  uid=uid,
                  language=ln,
                  req=req,
                  navmenuid='submit')
            else:
                return page_not_authorized(req, "direct",
                                           navmenuid='submit')

        return _index(req, **args)

    __call__ = index
