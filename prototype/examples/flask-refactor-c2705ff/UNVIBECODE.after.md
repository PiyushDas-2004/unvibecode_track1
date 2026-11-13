# UnvibeCode Map: flask_c2705ff

> The [UnvibeCode](https://github.com/FinanceFlash/unvibecode) Business Workflow Map and Connected Code Map for this repository, kept as text so git can diff it and every clone carries it.
> What does my change touch? `unvibe` · Refresh: `unvibecode-mapfile build` · Check a pull request: `unvibecode-mapfile check`
> Written by unvibecode-mapfile (community prototype, not an official UnvibeCode product). Do not edit by hand.

<!-- unvibecode-map:v1 source_files=102 connected_files=76 connections=232 unresolved_relative_imports=0 -->

## Business workflows

Not available yet: UnvibeCode's business analysis has not produced a workflow map for this repository. The sections below still work.

## Most-imported files

Change these with care: many files connect to them directly.

| File | Direct importers |
|---|---:|
| `tests/test_apps/cliapp/inner1/inner2/flask.py` | 43 |
| `src/flask/app.py` | 25 |
| `src/flask/typing.py` | 22 |
| `src/flask/globals.py` | 17 |
| `src/flask/wrappers.py` | 14 |
| `src/flask/helpers.py` | 12 |
| `src/flask/templating.py` | 11 |
| `examples/tutorial/flaskr/db.py` | 7 |
| `src/flask/sansio/app.py` | 7 |
| `src/flask/cli.py` | 6 |
| `src/flask/json/__init__.py` | 6 |
| `src/flask/sessions.py` | 6 |
| `src/flask/testing.py` | 6 |
| `src/flask/sansio/scaffold.py` | 5 |
| `src/flask/signals.py` | 5 |

## Area connections

| From | To | Connections |
|---|---|---:|
| `tests` | `src/flask` | 47 |
| `examples` | `src/flask` | 10 |
| `examples` | `tests` | 10 |
| `src/flask` | `tests` | 7 |

## Check these connections

These look wrong or surprising. Verify them; if UnvibeCode is wrong, report it upstream.

- `examples/celery/src/task_app/__init__.py` → `tests/test_apps/cliapp/inner1/inner2/flask.py` — non-test code connected into test code
- `examples/celery/src/task_app/views.py` → `tests/test_apps/cliapp/inner1/inner2/flask.py` — non-test code connected into test code
- `examples/javascript/js_example/__init__.py` → `tests/test_apps/cliapp/inner1/inner2/flask.py` — non-test code connected into test code
- `examples/javascript/js_example/views.py` → `tests/test_apps/cliapp/inner1/inner2/flask.py` — non-test code connected into test code
- `examples/tutorial/flaskr/__init__.py` → `tests/test_apps/cliapp/inner1/inner2/flask.py` — non-test code connected into test code
- `examples/tutorial/flaskr/auth.py` → `tests/test_apps/cliapp/inner1/inner2/flask.py` — non-test code connected into test code
- `examples/tutorial/flaskr/blog.py` → `tests/test_apps/cliapp/inner1/inner2/flask.py` — non-test code connected into test code
- `examples/tutorial/flaskr/db.py` → `tests/test_apps/cliapp/inner1/inner2/flask.py` — non-test code connected into test code
- `src/flask/app.py` → `tests/test_apps/helloworld/wsgi.py` — non-test code connected into test code
- `src/flask/cli.py` → `tests/test_apps/helloworld/wsgi.py` — non-test code connected into test code
- `src/flask/ctx.py` → `tests/test_apps/helloworld/wsgi.py` — non-test code connected into test code
- `src/flask/helpers.py` → `tests/conftest.py` · app_ctx — non-test code connected into test code
- `src/flask/testing.py` → `tests/test_apps/blueprintapp/apps/admin/static/css/test.css` — non-test code connected into test code
- `src/flask/testing.py` → `tests/test_apps/helloworld/wsgi.py` — non-test code connected into test code
- `src/flask/typing.py` → `tests/test_apps/helloworld/wsgi.py` — non-test code connected into test code
- 43 files → `tests/test_apps/cliapp/inner1/inner2/flask.py` — its name shadows the package `flask/`; imports of `flask` may be mis-resolved

## Coverage

- Source files analysed: 102
- Files with at least one connection: 76 (74%)
- Relative imports UnvibeCode could not resolve: 0

## Connections

One line per connected file pair, with the symbols used. Line numbers are left out on purpose, so this section only changes when structure changes.

### `examples/celery/src/task_app/__init__.py`
- → `examples/celery/src/task_app/views.py`
- → `src/flask/app.py` · Flask
- → `src/flask/templating.py` · render_template
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `examples/celery/src/task_app/views.py`
- → `examples/celery/src/task_app/tasks.py`
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `examples/javascript/js_example/__init__.py`
- → `src/flask/app.py` · Flask
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `examples/javascript/js_example/views.py`
- → `src/flask/json/__init__.py` · jsonify
- → `src/flask/templating.py` · render_template
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `examples/javascript/tests/test_js_example.py`
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `examples/tutorial/flaskr/__init__.py`
- → `examples/tutorial/flaskr/auth.py`
- → `examples/tutorial/flaskr/blog.py`
- → `examples/tutorial/flaskr/db.py`
- → `src/flask/app.py` · Flask
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `examples/tutorial/flaskr/auth.py`
- → `examples/tutorial/flaskr/db.py` · get_db
- → `src/flask/helpers.py` · flash, redirect, url_for
- → `src/flask/templating.py` · render_template
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `examples/tutorial/flaskr/blog.py`
- → `examples/tutorial/flaskr/auth.py` · login_required
- → `examples/tutorial/flaskr/db.py` · get_db
- → `src/flask/helpers.py` · flash, redirect, url_for
- → `src/flask/templating.py` · render_template
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `examples/tutorial/flaskr/db.py`
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `examples/tutorial/tests/conftest.py`
- → `examples/tutorial/flaskr/db.py` · get_db, init_db

### `examples/tutorial/tests/test_auth.py`
- → `examples/tutorial/flaskr/db.py` · get_db
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `examples/tutorial/tests/test_blog.py`
- → `examples/tutorial/flaskr/db.py` · get_db

### `examples/tutorial/tests/test_db.py`
- → `examples/tutorial/flaskr/db.py` · get_db

### `src/flask/__init__.py`
- → `src/flask/app.py` · Flask
- → `src/flask/blueprints.py` · Blueprint
- → `src/flask/config.py` · Config
- → `src/flask/ctx.py` · after_this_request, copy_current_request_context, has_app_context, has_request_context
- → `src/flask/globals.py`
- → `src/flask/helpers.py` · abort, flash, get_flashed_messages, get_template_attribute, make_response, redirect, send_file, send_from_directory, stream_with_context, url_for
- → `src/flask/json/__init__.py` · jsonify
- → `src/flask/signals.py`
- → `src/flask/templating.py` · render_template, render_template_string, stream_template, stream_template_string
- → `src/flask/wrappers.py` · Request, Response

### `src/flask/__main__.py`
- → `src/flask/cli.py` · main

### `src/flask/app.py`
- → `src/flask/cli.py`
- → `src/flask/ctx.py` · AppContext
- → `src/flask/debughelpers.py`
- → `src/flask/globals.py`
- → `src/flask/helpers.py` · get_debug_flag, get_flashed_messages, get_load_dotenv, send_from_directory
- → `src/flask/sansio/app.py` · App
- → `src/flask/sessions.py` · SecureCookieSessionInterface, SessionInterface
- → `src/flask/signals.py`
- → `src/flask/templating.py` · Environment
- → `src/flask/testing.py`
- → `src/flask/typing.py`
- → `src/flask/wrappers.py` · Request, Response
- → `tests/test_apps/helloworld/wsgi.py`

### `src/flask/blueprints.py`
- → `src/flask/cli.py` · AppGroup
- → `src/flask/globals.py`
- → `src/flask/helpers.py` · send_from_directory
- → `src/flask/sansio/blueprints.py` · Blueprint, BlueprintSetupState
- → `src/flask/sansio/scaffold.py`
- → `src/flask/typing.py`
- → `src/flask/wrappers.py`

### `src/flask/cli.py`
- → `src/flask/app.py`
- → `src/flask/globals.py`
- → `src/flask/helpers.py` · get_debug_flag, get_load_dotenv
- → `src/flask/typing.py`
- → `tests/test_apps/helloworld/wsgi.py`

### `src/flask/config.py`
- → `src/flask/sansio/app.py`
- → `src/flask/typing.py`

### `src/flask/ctx.py`
- → `src/flask/app.py`
- → `src/flask/globals.py`
- → `src/flask/sessions.py`
- → `src/flask/signals.py`
- → `src/flask/typing.py`
- → `src/flask/wrappers.py`
- → `tests/test_apps/helloworld/wsgi.py`

### `src/flask/debughelpers.py`
- → `src/flask/blueprints.py` · Blueprint
- → `src/flask/globals.py`
- → `src/flask/sansio/app.py` · App
- → `src/flask/sansio/scaffold.py`
- → `src/flask/typing.py`
- → `src/flask/wrappers.py`

### `src/flask/globals.py`
- → `src/flask/app.py`
- → `src/flask/ctx.py`
- → `src/flask/sessions.py`
- → `src/flask/typing.py`
- → `src/flask/wrappers.py`

### `src/flask/helpers.py`
- → `src/flask/globals.py`
- → `src/flask/signals.py`
- → `src/flask/typing.py`
- → `src/flask/wrappers.py` · Response
- → `tests/conftest.py` · app_ctx

### `src/flask/json/__init__.py`
- → `src/flask/globals.py`
- → `src/flask/json/provider.py` · _default
- → `src/flask/typing.py`
- → `src/flask/wrappers.py`

### `src/flask/json/provider.py`
- → `src/flask/sansio/app.py`
- → `src/flask/typing.py`

### `src/flask/json/tag.py`
- → `src/flask/json/__init__.py` · dumps, loads
- → `src/flask/typing.py`

### `src/flask/logging.py`
- → `src/flask/globals.py`
- → `src/flask/sansio/app.py`
- → `src/flask/typing.py`

### `src/flask/sansio/app.py`
- → `src/flask/config.py` · Config, ConfigAttribute
- → `src/flask/ctx.py` · _AppCtxGlobals
- → `src/flask/helpers.py` · _split_blueprint_path, get_debug_flag
- → `src/flask/json/provider.py` · DefaultJSONProvider, JSONProvider
- → `src/flask/logging.py` · create_logger
- → `src/flask/sansio/blueprints.py`
- → `src/flask/sansio/scaffold.py` · Scaffold, _endpoint_from_view_func, find_package, setupmethod
- → `src/flask/templating.py` · DispatchingJinjaLoader, Environment
- → `src/flask/testing.py`
- → `src/flask/typing.py`
- → `src/flask/wrappers.py`

### `src/flask/sansio/blueprints.py`
- → `src/flask/sansio/app.py`
- → `src/flask/sansio/scaffold.py` · Scaffold, _endpoint_from_view_func, setupmethod
- → `src/flask/typing.py`

### `src/flask/sansio/scaffold.py`
- → `src/flask/helpers.py` · get_root_path
- → `src/flask/templating.py` · _default_template_ctx_processor
- → `src/flask/typing.py`

### `src/flask/sessions.py`
- → `src/flask/app.py`
- → `src/flask/json/tag.py` · TaggedJSONSerializer
- → `src/flask/typing.py`
- → `src/flask/wrappers.py`

### `src/flask/templating.py`
- → `src/flask/app.py`
- → `src/flask/debughelpers.py`
- → `src/flask/globals.py`
- → `src/flask/helpers.py` · stream_with_context
- → `src/flask/sansio/app.py`
- → `src/flask/sansio/scaffold.py`
- → `src/flask/signals.py`
- → `src/flask/typing.py`

### `src/flask/testing.py`
- → `src/flask/app.py`
- → `src/flask/cli.py` · ScriptInfo
- → `src/flask/sessions.py` · SessionMixin
- → `src/flask/typing.py`
- → `src/flask/wrappers.py` · Request
- → `tests/test_apps/blueprintapp/apps/admin/static/css/test.css`
- → `tests/test_apps/helloworld/wsgi.py`

### `src/flask/typing.py`
- → `tests/test_apps/helloworld/wsgi.py`

### `src/flask/views.py`
- → `src/flask/globals.py`
- → `src/flask/typing.py`

### `src/flask/wrappers.py`
- → `src/flask/debughelpers.py`
- → `src/flask/globals.py`
- → `src/flask/helpers.py` · _split_blueprint_path
- → `src/flask/json/__init__.py`
- → `src/flask/typing.py`

### `tests/conftest.py`
- → `src/flask/app.py` · Flask
- → `src/flask/globals.py`
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `tests/test_appctx.py`
- → `src/flask/globals.py`
- → `tests/conftest.py` · app_ctx
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `tests/test_apps/blueprintapp/__init__.py`
- → `src/flask/app.py` · Flask
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `tests/test_apps/blueprintapp/apps/admin/__init__.py`
- → `src/flask/templating.py` · render_template
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `tests/test_apps/blueprintapp/apps/frontend/__init__.py`
- → `src/flask/templating.py` · render_template
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `tests/test_apps/cliapp/app.py`
- → `src/flask/app.py` · Flask
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `tests/test_apps/cliapp/factory.py`
- → `src/flask/app.py` · Flask
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `tests/test_apps/cliapp/importerrorapp.py`
- → `src/flask/app.py` · Flask
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `tests/test_apps/cliapp/inner1/__init__.py`
- → `src/flask/app.py` · Flask
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `tests/test_apps/cliapp/inner1/inner2/flask.py`
- → `src/flask/app.py` · Flask

### `tests/test_apps/cliapp/multiapp.py`
- → `src/flask/app.py` · Flask
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `tests/test_apps/helloworld/hello.py`
- → `src/flask/app.py` · Flask
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `tests/test_apps/helloworld/wsgi.py`
- → `tests/test_apps/helloworld/hello.py`

### `tests/test_apps/subdomaintestmodule/__init__.py`
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `tests/test_async.py`
- → `src/flask/app.py` · Flask
- → `src/flask/views.py` · MethodView, View
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `tests/test_basic.py`
- → `src/flask/debughelpers.py`
- → `src/flask/typing.py`
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `tests/test_blueprints.py`
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `tests/test_cli.py`
- → `src/flask/app.py` · Flask
- → `src/flask/cli.py` · AppGroup, FlaskGroup, NoAppException, ScriptInfo, find_best_app, get_version, load_dotenv, locate_app, prepare_import, run_command, with_appcontext
- → `src/flask/testing.py`
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `tests/test_config.py`
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `tests/test_converters.py`
- → `src/flask/helpers.py` · url_for
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `tests/test_helpers.py`
- → `src/flask/helpers.py` · get_debug_flag
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `tests/test_instance_config.py`
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `tests/test_json.py`
- → `src/flask/json/provider.py` · DefaultJSONProvider
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `tests/test_json_tag.py`
- → `src/flask/json/tag.py` · JSONTag, TaggedJSONSerializer

### `tests/test_logging.py`
- → `src/flask/logging.py` · has_level_handler, wsgi_errors_stream

### `tests/test_regression.py`
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `tests/test_reqctx.py`
- → `src/flask/globals.py`
- → `src/flask/sessions.py` · SecureCookieSessionInterface, SessionInterface
- → `src/flask/testing.py`
- → `tests/conftest.py` · app_ctx
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `tests/test_request.py`
- → `src/flask/app.py` · Flask
- → `src/flask/testing.py` · FlaskClient
- → `src/flask/wrappers.py` · Request
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `tests/test_session_interface.py`
- → `src/flask/globals.py`
- → `src/flask/sessions.py` · SessionInterface
- → `tests/conftest.py` · app_ctx
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `tests/test_signals.py`
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `tests/test_subclassing.py`
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `tests/test_templating.py`
- → `src/flask/logging.py`
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `tests/test_testing.py`
- → `src/flask/cli.py` · ScriptInfo
- → `src/flask/globals.py`
- → `src/flask/json/__init__.py` · jsonify
- → `src/flask/testing.py` · EnvironBuilder, FlaskCliRunner
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `tests/test_user_error_handler.py`
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `tests/type_check/typing_app_decorators.py`
- → `src/flask/app.py` · Flask
- → `src/flask/wrappers.py` · Response
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `tests/type_check/typing_error_handler.py`
- → `src/flask/app.py` · Flask
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`

### `tests/type_check/typing_route.py`
- → `src/flask/app.py` · Flask
- → `src/flask/json/__init__.py` · jsonify
- → `src/flask/templating.py` · render_template, stream_template
- → `src/flask/typing.py`
- → `src/flask/views.py` · View
- → `src/flask/wrappers.py` · Response
- → `tests/test_apps/cliapp/inner1/inner2/flask.py`
