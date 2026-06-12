# Testnet Burst Lab

Local-only workload benchmark rebuilt from the supplied interface.

It measures concurrent request throughput, synthetic fixture processing,
latency percentiles, planned misses, and clean cancellation behavior. It does
not generate or retain private keys, query balances, use proxies, or call
external services.

## Run

```powershell
npm install
npm run dev
```

Open `http://localhost:3000`.

## Verify

```powershell
npm run lint
npm run typecheck
npm run build
npm run smoke
```

## Benchmark model

- `Client lanes` controls concurrent browser requests.
- `Workers per request` controls logical server concurrency.
- `Batch size` controls fixtures processed per request.
- `Synthetic latency` models an asynchronous workload without network access.
- `Planned miss rate` creates expected negative results without logging them as
  runtime failures.

The identifiers beginning with `tb1qsim` are synthetic fixtures, not Bitcoin
addresses.
