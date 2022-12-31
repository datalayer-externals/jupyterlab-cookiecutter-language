# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import re
import sys

from babel import Locale
from copier_templates_extensions import ContextHook


# Regular expression that must respect a locale.
REGEX = re.compile(r"^\w{2}-\w{2}$")


class ContextUpdater(ContextHook):
    def hook(self, context):
        # Check locale
        locale = context["locale"]

        if not REGEX.match(locale):
            print(
                "ERROR: `locale` must be 4 letter code, like es-ES.\n"
                "       See http://www.lingoes.net/en/translator/langcode.htm"
            )
            sys.exit(1)

        locale_underscore = context["locale"].replace("-", "_")
        try:
            babel_locale = Locale.parse(locale_underscore)
            parsed_locale = babel_locale.language + "_" + babel_locale.territory
            # There is one exception for Norwegian
            if parsed_locale != locale_underscore and (parsed_locale != 'nb_NO' or locale_underscore != 'no_NO'):
                raise ValueError()
        except Exception:
            print("ERROR: Locale \"{0}\" is invalid!\n       See http://www.lingoes.net/en/translator/langcode.htm".format(locale))
            sys.exit(1)

        new_context = {}
        # Create an helper variable
        new_context["locale_underscore"] = locale_underscore
        return new_context
