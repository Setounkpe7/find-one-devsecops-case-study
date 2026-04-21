# Find-One — operational runbook (rollback + scan failure response)

> Excerpted from the source project's `docs/RUNBOOK.md`. Included here to document the operational side of the pipeline: what happens when a deploy breaks or a scan blocks a PR. Verbatim except for path redactions.

---

## 1. Production rollback

### Rollback via Vercel dashboard

1. Open the [Vercel dashboard](https://vercel.com) and navigate to the Find-One project.
2. Go to **Deployments**.
3. Find the last known-good deployment.
4. Click **⋯ → Promote to Production**.
5. Wait for the promotion to complete (~30 s).

### Verify rollback

```bash
curl -f https://<your-domain>/api/health
```

Expected: `{"status": "ok"}` with HTTP 200.

### Check current production version

```bash
vercel ls --prod
```

Or check the Deployments tab; the active deployment is marked Current.

---

## 2. Responding to blocking scan failures

### pip-audit (any vulnerability)

1. Open the pip-audit artifact from the failed CI run.
2. Note the vulnerable package and CVE.
3. Upgrade the package:
   ```bash
   pip install --upgrade <package>
   pip freeze | grep <package> >> backend/requirements.txt  # update pinned version
   ```
4. Confirm locally:
   ```bash
   pip-audit -r backend/requirements.txt
   ```
5. Commit and push:
   ```bash
   git add backend/requirements.txt
   git commit -m "fix: upgrade <package> to resolve CVE-XXXX-XXXXX"
   git push
   ```

---

### npm audit (CRITICAL severity)

1. Open the npm-audit artifact from the failed CI run.
2. Note the vulnerable package.
3. Auto-fix:
   ```bash
   cd frontend && npm audit fix
   ```
4. If `npm audit fix` cannot resolve it (breaking change required):
   ```bash
   npm audit fix --force   # test thoroughly after this
   ```
5. Commit and push:
   ```bash
   git add frontend/package.json frontend/package-lock.json
   git commit -m "fix: resolve CRITICAL npm vulnerability in <package>"
   git push
   ```

---

### Bandit (HIGH severity)

1. Open the Bandit artifact. Note the B-code and file location.
2. Common fixes:

   | B-code | Issue | Fix |
   |--------|-------|-----|
   | B608 | SQL injection via string formatting | Use SQLAlchemy ORM or parameterized queries |
   | B105/B106 | Hardcoded password in source | Move value to env var; read with `os.getenv()` |
   | B101 | `assert` used for security check | Replace with explicit `raise` |

3. Apply the fix, then confirm locally:
   ```bash
   bandit -r backend/app/ --severity-level HIGH --confidence-level MEDIUM
   ```
4. Commit and push.

---

### TruffleHog (verified secret in git history)

1. Rotate the secret immediately in the relevant service dashboard (Supabase, Anthropic, RapidAPI, etc.).
2. Update the new value in GitHub → Settings → Environments for the correct environment.
3. Remove the secret from git history:
   ```bash
   pip install git-filter-repo
   git filter-repo --path <file-containing-secret> --invert-paths
   # or to scrub a specific string:
   git filter-repo --replace-text <(echo '<old-secret>==>REMOVED')
   ```
4. Force-push (this rewrites history; coordinate with the team first):
   ```bash
   git push --force-with-lease origin dev
   git push --force-with-lease origin main
   ```
5. Confirm the secret is gone:
   ```bash
   docker run --rm -v $(pwd):/repo trufflesecurity/trufflehog:latest git file:///repo --only-verified
   ```
