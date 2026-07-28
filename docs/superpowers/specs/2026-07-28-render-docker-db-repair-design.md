# Render Docker DB Repair Design

## Goal

Repair the Render `/film/mypage` failure while preserving the original test
data and publish the corrected application as:

```text
docker.io/dudcks9572/filmatique:2.0
```

## Confirmed cause

The application model and queries require `reservation.status`, but the SQLite
database originally packaged in image `1.0` did not contain that column. The
repaired database supplied for this release is valid and contains:

- the `reservation.status` column with a `RESERVED` server default;
- two reservation rows, both with `RESERVED`;
- eight users, twenty movies, and 6,300 schedules;
- no broken reservation foreign-key references.

The current deployment also starts Flask's development server and includes a
`.flaskenv` file that enables the interactive debugger.

## Release design

### Database

Use the verified repaired `pybo.db` as the database packaged in image `2.0`.
This preserves the original test data and removes the immediate schema mismatch.

Add a tracked Alembic/Flask-Migrate baseline for the current schema and stop
ignoring the `migrations/` directory. Stamp the repaired database at the
baseline during image construction, then run `flask db upgrade` before each
application start. Future schema changes must be committed as migrations.

The SQLite database itself remains excluded from Git. It is supplied locally
as a Docker build input and copied into the image. No database credentials or
user data are committed to GitHub.

### Production runtime

Replace `flask run` with Gunicorn. Disable Flask debug mode explicitly and do
not copy local development secrets or Git metadata into the image. The
container listens on Render's `PORT`, defaulting to port 5000 for local tests.

The startup sequence is:

```text
flask db upgrade
→ gunicorn starts pybo:create_app()
```

If a migration fails, Gunicorn must not start. This prevents the application
from serving requests against an incompatible schema.

### Deployment

Build and test `dudcks9572/filmatique:2.0` locally before changing Render.
Verify login, `/film/mypage`, reservation data, and reservation cancellation.
Only after those checks pass should image `2.0` be pushed to Docker Hub and the
Render image reference changed from `1.0` to `2.0`.

The current Render service is not deleted. Changing the image reference gives
a clear rollback path to `1.0`, although `1.0` still contains the known
`reservation.status` defect.

## Tests and acceptance criteria

Automated checks must verify:

- the packaged SQLite database passes `PRAGMA integrity_check`;
- `reservation.status` exists and all existing reservations have a status;
- migration upgrade creates the current schema in a new empty SQLite database;
- the Flask app starts with debug mode disabled;
- an authenticated request to `/film/mypage` returns HTTP 200;
- the container starts with Gunicorn and responds on the configured port.

Release acceptance requires all automated checks to pass and a local container
smoke test to confirm the login and my-page flow.

## Known limitation

Render's free instance has no Persistent Disk. Image `2.0` preserves the
original test data, but registrations, reservations, cancellations, and other
changes made after deployment can be lost on a restart or redeploy. Moving the
application to Render PostgreSQL is a separate follow-up project and is the
recommended path before storing real user data.
